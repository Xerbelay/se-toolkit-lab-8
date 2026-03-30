# Observability Skill

Use observability tools when the user asks about:
- recent errors
- failing requests
- backend problems
- logs
- traces
- incidents
- whether something is broken
- what failed in the last N minutes

## Tool usage strategy

1. For scoped error questions, start with `logs_error_count`.
2. If there are errors, use `logs_search` with:
   - `service_name="Learning Management Service"` unless the user asks about another service
   - `severity="ERROR"`
   - a narrow recent time window
3. If you find a `trace_id` in logs, call `traces_get` for that trace.
4. If the user asks for recent traces, use `traces_list`.
5. Summarize findings briefly:
   - whether errors exist
   - which service they belong to
   - which event failed
   - trace ID if relevant
   - where the failure appears in the trace
6. Do not dump raw JSON unless the user explicitly asks for raw output.

## Default scope

If the user asks a broad observability question, prefer:
- service: `Learning Management Service`
- time window: last 10 minutes

## Example good flow

User: "Any LMS backend errors in the last 10 minutes?"

1. `logs_error_count(service_name="Learning Management Service", minutes=10)`
2. if errors > 0:
   - `logs_search(service_name="Learning Management Service", severity="ERROR", minutes=10, limit=20)`
3. if a `trace_id` appears:
   - `traces_get(trace_id=...)`
4. answer with a short summary
