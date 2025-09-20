├── config/
│   └── main_config.yaml
├── agents/
│   ├── base_agent.py          # Abstract base class for agents
│   ├── system_agent.py        # Handles prompt generation for system, SQL generation
│   ├── user_simulator_parser.py # Parses system responses for user simulator
│   └── user_simulator_generator.py # Generates user responses
├── pipeline/
│   ├── __init__.py
│   ├── ambiguity_resolution.py # Orchestrates Phase 1
│   ├── follow_up_question.py   # Orchestrates Phase 2
│   └── main_pipeline.py       # Main pipeline runner (combines phases)
├── utils/
│   ├── llm_api_caller.py      # Wrapper for LLM API calls
│   ├── data_handler.py        # Functions for loading/saving data (e.g., jsonl)
│   ├── schema_loader.py       # Loads DB schema and KB
│   └── logging_config.py      # Configures logging
├── models/
│   ├── __init__.py
│   ├── conversation.py        # Pydantic models for Conversation, Turn, Message
│   ├── database.py            # Pydantic models for DBSchema, ExternalKB
│   └── llm_response.py        # Pydantic model for LLM outputs
├── scripts/
│   └── run_pipeline.py        # Entry point to run the entire pipeline
├── state/
│   ├── conversation_state.py  # Manages conversation state
│   └── checkpoint_manager.py  # Handles checkpointing/recovery
├── middleware/
│   ├── rate_limiter.py       # API rate limiting
│   ├── retry_handler.py      # Retry logic with backoff
│   └── circuit_breaker.py    # Circuit breaker pattern
├── prompts/
│   ├── system/              # System agent prompts
│   ├── user_parser/         # User parser prompts  
│   └── user_generator/      # User generator prompts
└── requirements.txt
