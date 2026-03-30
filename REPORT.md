# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

Happy-path log excerpt:
```text
backend-1  | 2026-03-29 21:16:00,929 INFO [lms_backend.main] [main.py:62] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-29 21:16:00,932 INFO [lms_backend.auth] [auth.py:30] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-29 21:16:00,933 INFO [lms_backend.db.items] [items.py:16] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-29 21:16:01,033 INFO [lms_backend.main] [main.py:74] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.19.0.1:56122 - "GET /items/ HTTP/1.1" 200 OK
backend-1  | INFO:     172.19.0.1:56122 - "GET /items/ HTTP/1.1" 200
```

Error-path log excerpt:
```text
backend-1  | 2026-03-29 21:16:00,929 INFO [lms_backend.main] [main.py:62] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-29 21:16:00,932 INFO [lms_backend.auth] [auth.py:30] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-29 21:16:00,933 INFO [lms_backend.db.items] [items.py:16] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-29 21:16:01,033 INFO [lms_backend.main] [main.py:74] [trace_id=2886bef85c2f26a94b03e7c3ace88513 span_id=6908c67ce7586c3b resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.19.0.1:56122 - "GET /items/ HTTP/1.1" 200 OK
backend-1  | INFO:     172.19.0.1:56122 - "GET /items/ HTTP/1.1" 200
backend-1  | 2026-03-29 21:16:01,629 INFO [lms_backend.main] [main.py:62] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-29 21:16:01,630 INFO [lms_backend.auth] [auth.py:30] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-29 21:16:01,631 INFO [lms_backend.db.items] [items.py:16] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-29 21:16:14,123 ERROR [lms_backend.db.items] [items.py:23] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-29 21:16:14,123 WARNING [lms_backend.routers.items] [items.py:23] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - items_list_failed_as_not_found
backend-1  | 2026-03-29 21:16:14,124 INFO [lms_backend.main] [main.py:74] [trace_id=7cc4716409ec4aeece9281aa4d538efc span_id=f13a27dba19e4303 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.19.0.1:56132 - "GET /items/ HTTP/1.1" 404 Not Found
backend-1  | INFO:     172.19.0.1:56132 - "GET /items/ HTTP/1.1" 404
```

VictoriaLogs screenshot:
![VictoriaLogs query result](docs/task-3/victorialogs-errors.jpg)

## Task 3B — Traces

Healthy trace screenshot:
![Healthy trace](docs/task-3/victoriatraces-happy.png)

Error trace screenshot:
![Error trace](docs/task-3/victoriatraces-error.png)

## Task 3C — Observability MCP tools

Normal-condition response:
```text
Good news! There are **no LMS backend errors** in the last 10 minutes. The error count is 0, and the log search returned no ERROR entries for the LMS service.

The LMS backend appears to be running without issues during this time window.```

Failure-condition response:
```text
No LMS backend errors in the last 10 minutes. The error count is **0** and no ERROR log entries were found for the LMS service. The backend appears to be running smoothly.```

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
