"""
API client module for calling various language models.

This module provides a unified interface for calling different language model APIs
including OpenAI's GPT models. It handles authentication, request formatting,
and error handling with retry logic.
"""

import os
import time
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
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
    **kwargs: Any,
) -> str:
    """
    Call the underlying LLM endpoint with retry logic.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        engine: The model engine/name to use
        client: Initialized API client for the backend
        backend: Backend type ('openai', 'anthropic', etc.)
        **kwargs: Additional parameters passed to the API call

    Returns:
        The text response from the language model

    Raises:
        ValueError: If the backend is not supported
        RuntimeError: If all retry attempts fail
    """
    max_retries = 5
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            if backend == "openai":
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
            else:
                raise ValueError(f"Unsupported backend: {backend}")

        except Exception as e:
            print(f"API request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2**attempt))  # Exponential backoff
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
    stop: str | None | list[str] = None,
) -> str:
    """
    Set up the correct backend client and call the language model.

    Args:
        prompt: The prompt to send to the language model
        model_name: Name of the model to use (e.g., 'gpt-4.1-mini')
        temperature: Controls randomness in generation (0.0 to 2.0)
        max_tokens: Maximum number of tokens to generate
        top_p: Nucleus sampling parameter (0.0 to 1.0)
        frequency_penalty: Penalty for frequent tokens (-2.0 to 2.0)
        presence_penalty: Penalty for new tokens (-2.0 to 2.0)
        stop: Stop sequences to halt generation

    Returns:
        The text response from the language model

    Raises:
        ValueError: If the model is not supported or configuration is invalid
        RuntimeError: If the API call fails after retries
    """
    if not prompt:
        raise ValueError("Prompt cannot be empty")

    if not model_name:
        raise ValueError("Prompt cannot be empty")

    # Determine backend and set up client
    if "gpt" in model_name.lower():
        if model_name not in MODEL_CONFIG:
            raise ValueError(f"Model '{model_name}' not found in configuration")

        config = MODEL_CONFIG[model_name]
        if not config["api_key"]:
            raise ValueError(f"API key not configured for model '{model_name}'")

        engine = model_name
        client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
        )
        backend = "openai"
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # Convert dataclass to dict for kwargs
    kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop": stop,
    }
    messages = [{"role": "user", "content": prompt}]
    return api_request(messages, engine, client, backend, **kwargs)
