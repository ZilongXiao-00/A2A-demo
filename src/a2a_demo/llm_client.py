import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.json"


class LLMConfigError(RuntimeError):
    """本地 LLM 配置缺失或不完整时抛出。"""


def load_llm_config() -> dict[str, str]:
    """从环境变量或 config.json 读取 OpenAI-compatible LLM 配置。"""
    config: dict[str, str] = {}
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            raw_config = json.load(f)
        config.update({key: str(value) for key, value in raw_config.items() if value})

    env_map = {
        "base_url": "LLM_BASE_URL",
        "api_key": "LLM_API_KEY",
        "model": "LLM_MODEL",
    }
    for key, env_name in env_map.items():
        value = os.getenv(env_name)
        if value:
            config[key] = value

    missing = [key for key in env_map if not config.get(key)]
    if missing:
        missing_text = ", ".join(missing)
        raise LLMConfigError(
            f"Missing LLM configuration: {missing_text}. "
            "Set LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL, or create config.json."
        )
    return config


def call_llm(
    query: str,
    system_prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    tools: list[dict[str, Any]] | None = None,
    top_p: float = 0.9,
) -> str:
    """调用任意兼容 OpenAI Chat Completions 的 LLM 接口。"""
    config = load_llm_config()
    client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
    kwargs: dict[str, Any] = {
        "model": model or config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "temperature": temperature,
        "top_p": top_p,
    }
    if tools:
        kwargs["tools"] = tools

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""
