import json
import os
from pathlib import Path

APP_DIR = Path("/app/nanobot")
CONFIG_PATH = APP_DIR / "config.json"
RESOLVED_CONFIG_PATH = Path("/tmp/config.resolved.json")
WORKSPACE_PATH = APP_DIR / "workspace"
NANOBOT_BIN = APP_DIR / ".venv" / "bin" / "nanobot"
VENV_PYTHON = APP_DIR / ".venv" / "bin" / "python"


def set_if(value, target, key):
    if value is not None and value != "":
        target[key] = value


def main():
    cfg = json.loads(CONFIG_PATH.read_text())

    cfg.setdefault("agents", {}).setdefault("defaults", {})
    cfg.setdefault("providers", {}).setdefault("custom", {})
    cfg.setdefault("gateway", {})
    cfg.setdefault("channels", {})
    cfg["channels"].setdefault("webchat", {})
    cfg.setdefault("tools", {}).setdefault("mcpServers", {})
    cfg["tools"]["mcpServers"].setdefault("lms", {})
    cfg["tools"]["mcpServers"].setdefault("webchat_ui", {})
    cfg["tools"]["mcpServers"].setdefault("obs", {})

    set_if(os.environ.get("LLM_API_KEY"), cfg["providers"]["custom"], "apiKey")
    set_if(os.environ.get("LLM_API_BASE_URL"), cfg["providers"]["custom"], "apiBase")
    set_if(os.environ.get("LLM_API_MODEL"), cfg["agents"]["defaults"], "model")

    cfg["agents"]["defaults"]["provider"] = "custom"
    cfg["agents"]["defaults"]["workspace"] = str(WORKSPACE_PATH)

    set_if(os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"), cfg["gateway"], "host")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")
    if gateway_port:
        cfg["gateway"]["port"] = int(gateway_port)

    webchat = cfg["channels"]["webchat"]
    webchat["enabled"] = True
    webchat["allowFrom"] = ["*"]
    set_if(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"), webchat, "host")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    if webchat_port:
        webchat["port"] = int(webchat_port)

    lms = cfg["tools"]["mcpServers"]["lms"]
    lms["command"] = str(VENV_PYTHON)
    lms["args"] = ["-m", "mcp_lms", os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000")]
    lms["env"] = {
        "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000"),
        "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", ""),
        "LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", ""),
    }

    webchat_ui = cfg["tools"]["mcpServers"]["webchat_ui"]
    webchat_ui["command"] = str(VENV_PYTHON)
    webchat_ui["args"] = ["-m", "mcp_webchat"]
    webchat_ui["env"] = {
        "NANOBOT_WEBCHAT_UI_RELAY_URL": os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_URL", ""),
        "NANOBOT_WEBCHAT_UI_TOKEN": os.environ.get("NANOBOT_ACCESS_KEY", ""),
    }

    obs = cfg["tools"]["mcpServers"]["obs"]
    obs["command"] = str(VENV_PYTHON)
    obs["args"] = ["-m", "mcp_obs"]
    obs["env"] = {
        "MCP_OBS_LOGS_URL": os.environ.get("MCP_OBS_LOGS_URL", "http://victorialogs:9428"),
        "MCP_OBS_TRACES_URL": os.environ.get("MCP_OBS_TRACES_URL", "http://victoriatraces:10428"),
        "MCP_OBS_DEFAULT_SERVICE_NAME": os.environ.get("MCP_OBS_DEFAULT_SERVICE_NAME", "Learning Management Service"),
        "MCP_OBS_TIMEOUT_SECONDS": os.environ.get("MCP_OBS_TIMEOUT_SECONDS", "15"),
    }

    RESOLVED_CONFIG_PATH.write_text(json.dumps(cfg, indent=2))

    os.execv(
        str(NANOBOT_BIN),
        [
            str(NANOBOT_BIN),
            "gateway",
            "--config",
            str(RESOLVED_CONFIG_PATH),
            "--workspace",
            str(WORKSPACE_PATH),
        ],
    )


if __name__ == "__main__":
    main()
