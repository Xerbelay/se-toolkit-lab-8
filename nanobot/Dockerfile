FROM harbor.pg.innopolis.university/docker-hub-cache/astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

COPY . /app/nanobot
COPY --from=workspace /mcp /app/mcp
COPY --from=workspace /nanobot-websocket-channel /app/nanobot-websocket-channel

RUN --mount=type=cache,target=/root/.cache/uv \
    cd /app/nanobot && uv sync


FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14.2-slim-bookworm

ARG APP_UID=1000
ARG APP_GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends bash gosu && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${APP_GID} appgroup \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home appuser

WORKDIR /app

COPY --from=builder /app /app
RUN chown -R ${APP_UID}:${APP_GID} /app

USER appuser

CMD ["python", "/app/nanobot/entrypoint.py"]
