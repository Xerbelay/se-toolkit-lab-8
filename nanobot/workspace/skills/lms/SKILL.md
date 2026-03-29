---
name: lms
description: Use LMS MCP tools for live LMS data
always: true
---

You have access to live LMS data through MCP tools. Prefer LMS tools over guessing whenever the user asks about labs, backend health, learners, pass rates, completion, timeline, groups, or top performers.

Available LMS tools:
- lms_health: check whether the LMS backend is healthy and how many items are available
- lms_labs: list labs available in the LMS
- lms_learners: list learners
- lms_pass_rates: show pass-rate metrics for a lab
- lms_timeline: show timeline or submission activity for a lab
- lms_groups: show group-related metrics for a lab
- lms_top_learners: show top learners for a lab
- lms_completion_rate: show completion rate for a lab
- lms_sync_pipeline: trigger LMS sync if data appears missing

Behavior rules:
- If the user asks about scores, pass rates, completion, groups, timeline, top learners, or performance and does not specify a lab, call lms_labs first and ask the user to choose a lab.
- If the user asks whether the LMS is working, use lms_health.
- If the user asks what labs are available, use lms_labs.
- If data is missing or suspiciously empty, check lms_health and consider lms_sync_pipeline.
- Say when the answer comes from live LMS data.
- Do not invent LMS results.
- Keep answers concise and clear.
