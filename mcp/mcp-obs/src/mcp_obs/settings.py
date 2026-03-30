from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    logs_url: str
    traces_url: str
    default_service_name: str
    request_timeout_seconds: float


def resolve_settings() -> Settings:
    return Settings(
        logs_url=os.environ.get("MCP_OBS_LOGS_URL", "http://victorialogs:9428").rstrip("/"),
        traces_url=os.environ.get("MCP_OBS_TRACES_URL", "http://victoriatraces:10428").rstrip("/"),
        default_service_name=os.environ.get("MCP_OBS_DEFAULT_SERVICE_NAME", "Learning Management Service"),
        request_timeout_seconds=float(os.environ.get("MCP_OBS_TIMEOUT_SECONDS", "15")),
    )
