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
- "What went wrong?"
- "Check system health"

## Mandatory rules for this lab

1. For LMS/backend observability questions, ALWAYS use the exact service name:
   `Learning Management Service`

2. Never answer "What went wrong?" from memory.

3. For `What went wrong?` in this lab, DO NOT start with:
   - `mcp_lms_lms_health`
   - `mcp_lms_lms_sync_pipeline`
   - broad recovery actions

4. For `What went wrong?` use this exact flow:
   - `logs_error_count(service_name="Learning Management Service", minutes=10)`
   - if errors > 0:
     `logs_search(service_name="Learning Management Service", severity="ERROR", minutes=10, limit=20)`
   - extract the MOST RECENT relevant `trace_id`
   - `traces_get(trace_id=...)`

5. Focus on the newest failing `/items/` request from the last 10 minutes.

6. The expected discrepancy in this lab is:
   - logs and traces show a real PostgreSQL / SQLAlchemy / database failure
   - but the backend response path misreports it as `404 Items not found`

7. Your final answer must explicitly mention:
   - log evidence
   - trace evidence
   - affected service
   - failing operation
   - the mismatch between the real DB failure and the misleading 404 response

## Good answer shape

A short investigation summary:
- Recent LMS backend errors were found
- Logs show DB/backend failure
- Trace <id> shows the failing operation/span
- The backend incorrectly surfaced it as `404 Items not found`
