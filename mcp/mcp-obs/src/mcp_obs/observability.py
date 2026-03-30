from __future__ import annotations

from collections import Counter
import json
import re
from typing import Any

import httpx

from mcp_obs.settings import Settings


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _keyword_fragment(keyword: str) -> str:
    keyword = keyword.strip()
    if not keyword:
        return ""
    if re.fullmatch(r"[\w.\-:/]+", keyword):
        return keyword
    return _quote(keyword)


def _parse_response_text(text: str) -> list[dict[str, Any]]:
    text = text.strip()
    if not text:
        return []

    if text.startswith("{") or text.startswith("["):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [x for x in parsed if isinstance(x, dict)]
            if isinstance(parsed, dict):
                if isinstance(parsed.get("rows"), list):
                    return [x for x in parsed["rows"] if isinstance(x, dict)]
                if isinstance(parsed.get("data"), list):
                    return [x for x in parsed["data"] if isinstance(x, dict)]
                return [parsed]
        except json.JSONDecodeError:
            pass

    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                rows.append(obj)
            else:
                rows.append({"_raw": obj})
        except json.JSONDecodeError:
            rows.append({"_raw": line})
    return rows


def _simplify_log_entry(entry: dict[str, Any]) -> dict[str, Any]:
    preferred_keys = [
        "_time",
        "service.name",
        "severity",
        "event",
        "trace_id",
        "span_id",
        "_msg",
        "msg",
        "message",
        "status_code",
        "http.status_code",
        "error",
        "exception.type",
        "exception.message",
    ]
    out: dict[str, Any] = {}
    for key in preferred_keys:
        if key in entry:
            out[key] = entry[key]

    if not out:
        for key, value in entry.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                out[key] = value
                if len(out) >= 10:
                    break
    return out


def _span_has_error(span: dict[str, Any]) -> bool:
    for tag in span.get("tags", []):
        key = tag.get("key")
        value = tag.get("value")
        if key == "error" and str(value).lower() in {"1", "true", "yes"}:
            return True
        if key == "otel.status_code" and str(value).upper() == "ERROR":
            return True
    return False


class ObservabilityClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def _get_text(self, url: str, params: dict[str, Any] | None = None) -> str:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.text

    async def _get_json(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()

    async def logs_search(
        self,
        keyword: str = "",
        service_name: str = "",
        severity: str = "",
        minutes: int = 10,
        limit: int = 20,
    ) -> dict[str, Any]:
        service_name = service_name or self.settings.default_service_name

        parts: list[str] = [f"_time:{minutes}m"]
        if service_name:
            parts.append(f"service.name:{_quote(service_name)}")
        if severity:
            parts.append(f"severity:{severity.upper()}")
        keyword_part = _keyword_fragment(keyword)
        if keyword_part:
            parts.append(keyword_part)

        query = " ".join(parts)
        text = await self._get_text(
            f"{self.settings.logs_url}/select/logsql/query",
            params={"query": query, "limit": limit},
        )
        entries = _parse_response_text(text)

        return {
            "query": query,
            "count": len(entries),
            "entries": [_simplify_log_entry(x) for x in entries[:limit]],
        }

    async def logs_error_count(
        self,
        service_name: str = "",
        minutes: int = 10,
        limit: int = 200,
    ) -> dict[str, Any]:
        service_name = service_name or self.settings.default_service_name
        result = await self.logs_search(
            keyword="",
            service_name=service_name,
            severity="ERROR",
            minutes=minutes,
            limit=limit,
        )

        counter: Counter[str] = Counter()
        for entry in result["entries"]:
            svc = str(entry.get("service.name", service_name or "unknown"))
            counter[svc] += 1

        return {
            "query": result["query"],
            "window_minutes": minutes,
            "total_errors": sum(counter.values()),
            "services": [
                {"service.name": svc, "error_count": count}
                for svc, count in counter.most_common()
            ],
        }

    def _trace_services(self, trace: dict[str, Any]) -> list[str]:
        processes = trace.get("processes", {})
        names = {
            proc.get("serviceName", "unknown")
            for proc in processes.values()
            if isinstance(proc, dict)
        }
        return sorted(names)

    def _span_service_name(self, trace: dict[str, Any], span: dict[str, Any]) -> str:
        process_id = span.get("processID")
        process = trace.get("processes", {}).get(process_id, {})
        return process.get("serviceName", "unknown")

    def _summarize_trace_brief(self, trace: dict[str, Any]) -> dict[str, Any]:
        spans = trace.get("spans", [])
        error_spans = sum(1 for span in spans if _span_has_error(span))
        trace_id = trace.get("traceID") or (spans[0].get("traceID") if spans else None)

        return {
            "trace_id": trace_id,
            "span_count": len(spans),
            "error_span_count": error_spans,
            "services": self._trace_services(trace),
        }

    def _summarize_trace_full(self, trace: dict[str, Any]) -> dict[str, Any]:
        spans = trace.get("spans", [])
        spans_sorted = sorted(spans, key=lambda s: s.get("startTime", 0))

        out_spans = []
        for span in spans_sorted:
            out_spans.append(
                {
                    "span_id": span.get("spanID"),
                    "operation": span.get("operationName"),
                    "service.name": self._span_service_name(trace, span),
                    "start_time": span.get("startTime"),
                    "duration_ms": round(float(span.get("duration", 0)) / 1000.0, 2),
                    "error": _span_has_error(span),
                }
            )

        trace_id = trace.get("traceID") or (spans_sorted[0].get("traceID") if spans_sorted else None)

        return {
            "trace_id": trace_id,
            "span_count": len(spans_sorted),
            "error_span_count": sum(1 for span in spans_sorted if _span_has_error(span)),
            "services": self._trace_services(trace),
            "spans": out_spans,
        }

    async def traces_list(
        self,
        service_name: str = "",
        limit: int = 5,
    ) -> dict[str, Any]:
        service_name = service_name or self.settings.default_service_name
        payload = await self._get_json(
            f"{self.settings.traces_url}/select/jaeger/api/traces",
            params={"service": service_name, "limit": limit},
        )
        traces = payload.get("data", [])

        return {
            "service_name": service_name,
            "count": len(traces),
            "traces": [self._summarize_trace_brief(trace) for trace in traces],
        }

    async def traces_get(self, trace_id: str) -> dict[str, Any]:
        payload = await self._get_json(
            f"{self.settings.traces_url}/select/jaeger/api/traces/{trace_id}"
        )
        traces = payload.get("data", [])
        if not traces:
            return {"trace_id": trace_id, "found": False}
        return {"found": True, "trace": self._summarize_trace_full(traces[0])}
