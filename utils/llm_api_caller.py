import os
import logging
import time
from typing import Dict, Any

# We'll use the official OpenAI library. Add 'openai' to your requirements.txt
import openai
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

from models.config import AppConfig, ModelConfig

# Get a logger for this module
logger = logging.getLogger(__name__)

class LLMAPICaller:
    """
    A robust, centralized client for making calls to LLM APIs.

    This class handles:
    - Loading API keys securely from environment variables.
    - Configuring the API client with settings like timeouts and retries.
    - Providing a simple `call` method for agents to use.
    - In-memory caching to reduce redundant API calls and costs during a run.
    - Graceful handling of common API errors (e.g., rate limits, server errors).
    """

    def __init__(self, config: AppConfig):
        """
        Initializes the LLMAPICaller.

        Args:
            config (AppConfig): The application's configuration object.

        Raises:
            ValueError: If the required API key is not found in environment variables.
        """
        self.config = config
        self.client = self._initialize_client()
        
        if self.config.features.result_caching:
            self.cache: Dict[str, str] = {}
            logger.info("LLM result caching is ENABLED.")
        else:
            self.cache = None
            logger.info("LLM result caching is DISABLED.")

    def _initialize_client(self) -> OpenAI:
        """
        Loads the API key and initializes the OpenAI client.
        """
        api_key_env_var = self.config.credentials.openai_api_key.replace("env:", "")
        api_key = os.getenv(api_key_env_var)

        if not api_key:
            raise ValueError(
                f"OpenAI API key not found. Please set the '{api_key_env_var}' environment variable."
            )
        
        logger.info("OpenAI client initialized successfully.")
        return OpenAI(
            api_key=api_key,
            # The OpenAI client library uses tenacity for retries by default.
            # We can configure it with values from our config.
            max_retries=self.config.api.retry_config.max_retries,
            timeout=30.0, # A default timeout, can be overridden per call
        )

    def call(self, model_key: str, prompt: str, **kwargs: Any) -> str:
        """
        Makes a call to the specified LLM, with caching and error handling.

        Args:
            model_key (str): The key of the model in the config (e.g., 'system_model').
            prompt (str): The prompt to send to the LLM.
            **kwargs: Optional overrides for model parameters (e.g., temperature).

        Returns:
            The content of the LLM's response as a string.
        """
        # 1. Determine the final model configuration
        try:
            base_model_config = getattr(self.config.models, model_key)
        except AttributeError:
            logger.error(f"Model key '{model_key}' not found in configuration.")
            raise ValueError(f"Invalid model key: {model_key}")
            
        # Merge base config with any runtime overrides
        final_params = base_model_config.model_dump()
        final_params.update(kwargs)
        
        # Extract parameters relevant to the API call
        model_name = final_params.pop('name')
        timeout = final_params.pop('timeout')
        # 'retry_attempts' is handled by the client's `max_retries` config

        # 2. Check cache first
        cache_key = self._generate_cache_key(model_name, prompt, final_params)
        if self.cache is not None and cache_key in self.cache:
            logger.info(f"Cache hit for model '{model_name}'. Returning cached response.")
            return self.cache[cache_key]

        logger.info(f"Cache miss. Calling API for model '{model_name}'...")

        # 3. Make the API call with retry logic
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout,
                **final_params
            )
            duration = time.time() - start_time
            logger.info(f"API call successful. Duration: {duration:.2f}s")
            
            response_content = response.choices[0].message.content
            if response_content is None:
                logger.warning("API returned a null response content.")
                response_content = ""

            # 4. Store in cache if enabled
            if self.cache is not None:
                self.cache[cache_key] = response_content

            return response_content.strip()

        except RateLimitError as e:
            logger.error(f"Rate limit exceeded for model '{model_name}'. Please check your plan and usage. Error: {e}")
            return f"Error: Rate limit exceeded. {e}"
        except APITimeoutError as e:
            logger.error(f"API call timed out after {timeout}s for model '{model_name}'. Error: {e}")
            return f"Error: API timeout. {e}"
        except APIError as e:
            logger.error(f"An API error occurred for model '{model_name}'. Status: {e.status_code}. Error: {e.message}")
            return f"Error: API error. {e.message}"
        except Exception as e:
            logger.exception(f"An unexpected error occurred during the API call for model '{model_name}'.")
            return f"Error: An unexpected error occurred. {e}"

    def _generate_cache_key(self, model_name: str, prompt: str, params: Dict[str, Any]) -> str:
        """Creates a unique, deterministic key for caching."""
        # Sort params by key to ensure consistent key generation
        sorted_params = sorted(params.items())
        return f"{model_name}::{str(sorted_params)}::{prompt}"