"""
API client module for calling various language models.

This module provides a unified interface for calling different language model APIs
including OpenAI's GPT models. It handles authentication, request formatting,
and error handling with retry logic.
"""

import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

MODEL_CONFIG: dict[str, dict[str, str]] = {
    "gpt-4.1-mini": {
        "base_url": "https://api.openai.com/v1",
        "api_key": OPENAI_API_KEY,
    },
}


def api_request(
    messages: list[dict[str, str]],
    engine: str,
    client: OpenAI,
    backend: str = "openai",
    mode: str = "chat",
    text_format: Any = None,
    **kwargs: Any,
) -> Any:
    """
    Call the underlying LLM endpoint with retry logic.

    Args:
        messages: List of message dicts with 'role' and 'content'
        engine: Model engine/name
        client: Initialized API client
        backend: Backend type
        mode: "chat" or "structured"
        text_format: Pydantic model for structured output
        **kwargs: Additional API params

    Returns:
        Text response or structured output

    Raises:
        ValueError, RuntimeError
    """
    max_retries = 5
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            if backend == "openai":
                if mode == "chat":
                    completion = client.chat.completions.create(
                        model=engine,
                        messages=messages,
                        temperature=kwargs.get("temperature", 0.0),
                        max_tokens=kwargs.get("max_tokens", 512),
                        top_p=kwargs.get("top_p", 1.0),
                        frequency_penalty=kwargs.get("frequency_penalty", 0.0),
                        presence_penalty=kwargs.get("presence_penalty", 0.0),
                        stop=kwargs.get("stop", None),
                    )
                    return completion.choices[0].message.content or ""
                elif mode == "structured":
                    if text_format is None:
                        raise ValueError(
                            "`text_format` must be provided for structured mode"
                        )
                    response = client.responses.parse(
                        model=engine,
                        input=messages,
                        text_format=text_format,
                    )
                    return response.output_parsed
                else:
                    raise ValueError("mode must be 'chat' or 'structured'")
            else:
                raise ValueError(f"Unsupported backend: {backend}")
        except Exception as e:
            print(f"API request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2**attempt))
            else:
                raise RuntimeError(f"All retry attempts failed. Last error: {e}")


def get_query_response(
    prompt: str,
    model_name: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: str | list[str] | None = None,
    mode: str = "chat",
    text_format: Any = None,
) -> Any:
    """
    Set up the correct backend client and call the language model.

    Args:
        prompt: Prompt to send
        model_name: Model name (e.g., 'gpt-4.1-mini')
        temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop: API params
        mode: "chat" or "structured"
        text_format: Pydantic model for structured output

    Returns:
        Text response or structured output

    Raises:
        ValueError, RuntimeError
    """
    if not prompt:
        raise ValueError("`prompt` cannot be empty")
    if (
        not model_name
        or "gpt" not in model_name.lower()
        or model_name not in MODEL_CONFIG
    ):
        raise ValueError(f"Model '{model_name}' not found or unsupported")

    config = MODEL_CONFIG[model_name]
    if not config["api_key"]:
        raise ValueError(f"API key not configured for model '{model_name}'")

    engine = model_name
    client = OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
    )
    backend = "openai"
    messages = [{"role": "user", "content": prompt}]

    if mode not in ("chat", "structured"):
        raise ValueError("mode must be 'chat' or 'structured'")

    return api_request(
        messages=messages,
        engine=engine,
        client=client,
        backend=backend,
        mode=mode,
        text_format=text_format,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
