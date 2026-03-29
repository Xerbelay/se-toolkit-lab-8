#!/usr/bin/env bash
set -euo pipefail

export NANOBOT_LMS_BACKEND_URL="http://localhost:42002"
export NANOBOT_LMS_API_KEY="$(grep '^LMS_API_KEY=' /root/se-toolkit-lab-8/.env.docker.secret | cut -d= -f2-)"

exec python -m mcp_lms "http://localhost:42002"
