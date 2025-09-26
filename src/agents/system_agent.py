import logging
from models.conversation import Conversation, Message
from utils.llm_api_caller import LLMAPICaller

logger = logging.getLogger(__name__)

class SystemAgent:
    def __init__(self, config, system_model_config, llm_caller: LLMAPICaller):
        self.config = config
        self.model_config = system_model_config
        self.llm_caller = llm_caller
        # Here you would load prompt templates from self.config.prompt_templates_dir

    def act(self, conversation: Conversation) -> Message:
        """
        Analyzes the conversation and decides whether to ask a clarifying
        question or generate the final SQL query.
        """
        logger.debug("System Agent is thinking...")
        
        # 1. Construct the prompt from the conversation history
        # This is the core logic from the original `infer_api_system.py`
        prompt = self._build_prompt(conversation)

        # 2. Call the LLM via the utility
        raw_response = self.llm_caller.call(
            model_name=self.model_config.name,
            prompt=prompt
        )

        # 3. Parse the raw response and format it as a Message object
        # This logic comes from `collect_response.py`
        formatted_content = self._parse_llm_response(raw_response)
        
        return Message(role="system", content=formatted_content)

    def _build_prompt(self, conversation: Conversation) -> str:
        # Complex logic to build the exact prompt string goes here.
        # It would use the loaded Jinja2 templates.
        return f"Conversation history: {conversation.to_string()}\n\nWhat is the next step?"

    def _parse_llm_response(self, raw_response: str) -> str:
        # Logic to clean up and structure the LLM's output.
        return raw_response.strip()

    def extract_sql(self, conversation: Conversation) -> str:
        # Logic from `wrap_up_sql.py` to find and clean the SQL query.
        for message in reversed(conversation.messages):
            if "[SQL]" in message.content:
                # Add extraction logic here
                return message.content
        return ""