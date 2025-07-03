import os
from langchain_openai import ChatOpenAI

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL") or None
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME") or "gpt-4o-mini"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise NotImplementedError("OPENAI_API_KEY is required")

def get_openai_llm(
    model: str = None,
    api_key: str = None,
    base_url: str = None,
    **kwargs
):
    params = {
        "model": model or OPENAI_MODEL_NAME,
        "api_key": api_key or OPENAI_API_KEY,
    }
    if base_url or OPENAI_BASE_URL:
        params["base_url"] = base_url or OPENAI_BASE_URL
    params.update(kwargs)
    return ChatOpenAI(**params)
