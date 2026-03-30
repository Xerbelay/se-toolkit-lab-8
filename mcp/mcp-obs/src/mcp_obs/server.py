from mcp.server.fastmcp import FastMCP

from mcp_obs.observability import ObservabilityClient
from mcp_obs.settings import resolve_settings

settings = resolve_settings()
client = ObservabilityClient(settings)

mcp = FastMCP("obs")


@mcp.tool()
async def logs_search(
    keyword: str = "",
    service_name: str = "",
    severity: str = "",
    minutes: int = 10,
    limit: int = 20,
) -> dict:
    """Search recent VictoriaLogs entries by keyword, service and severity."""
    return await client.logs_search(
        keyword=keyword,
        service_name=service_name,
        severity=severity,
        minutes=minutes,
        limit=limit,
    )


@mcp.tool()
async def logs_error_count(
    service_name: str = "",
    minutes: int = 10,
) -> dict:
    """Count recent ERROR log entries for a service."""
    return await client.logs_error_count(
        service_name=service_name,
        minutes=minutes,
    )


@mcp.tool()
async def traces_list(
    service_name: str = "",
    limit: int = 5,
) -> dict:
    """List recent traces for a service from VictoriaTraces."""
    return await client.traces_list(
        service_name=service_name,
        limit=limit,
    )


@mcp.tool()
async def traces_get(trace_id: str) -> dict:
    """Fetch and summarize a specific trace by ID."""
    return await client.traces_get(trace_id=trace_id)
