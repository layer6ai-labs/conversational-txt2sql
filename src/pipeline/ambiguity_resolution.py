# pipeline/ambiguity_resolution.py

import logging

from models.config import AppConfig
from models.conversation import Conversation
from agents.system_agent import SystemAgent
from agents.user_simulator_parser import UserSimulatorParserAgent
from agents.user_simulator_generator import UserSimulatorGeneratorAgent
from utils.data_handler import DataHandler

logger = logging.getLogger(__name__)

class AmbiguityResolutionRunner:
    """
    Manages the multi-turn conversation to resolve ambiguities and generate SQL.
    """
    def __init__(self, config: AppConfig, system_agent: SystemAgent, user_parser: UserSimulatorParserAgent, user_generator: UserSimulatorGeneratorAgent, data_handler: DataHandler):
        self.config = config
        self.system_agent = system_agent
        self.user_parser = user_parser
        self.user_generator = user_generator
        self.data_handler = data_handler

    def run(self, initial_conversation: Conversation) -> (Conversation, str):
        """
        Executes the conversational loop for Phase 1.
        """
        logger.info("--- Executing Phase: Ambiguity Resolution ---")
        conversation = initial_conversation
        phase_config = self.config.pipeline.phases.ambiguity_resolution

        for turn_num in range(1, phase_config.max_turns + 1):
            logger.info(f"Starting Turn {turn_num}")

            system_message = self.system_agent.act(conversation, phase='ambiguity_resolution')
            conversation.add_message(system_message)

            if "[SQL]" in system_message.content:
                logger.info("System agent generated SQL. Concluding phase.")
                break

            parsed_intent = self.user_parser.act(system_message)
            user_message = self.user_generator.act(conversation, parsed_intent)
            conversation.add_message(user_message)

        final_sql = self.system_agent.extract_sql(conversation)
        self.data_handler.save_sql_result(final_sql, self.config.data.file_patterns.sql_results)
        return conversation, final_sql