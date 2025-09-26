# pipeline/debugging.py

import logging

from models.config import AppConfig
from models.conversation import Conversation
from agents.system_agent import SystemAgent
from utils.data_handler import DataHandler

logger = logging.getLogger(__name__)

class DebuggingRunner:
    """
    Manages a single-turn debugging attempt on a failed SQL query.
    """
    def __init__(self, config: AppConfig, system_agent: SystemAgent, data_handler: DataHandler):
        self.config = config
        self.system_agent = system_agent
        self.data_handler = data_handler

    def run(self, conversation: Conversation, original_sql: str, execution_error: str) -> str:
        """
        Executes the debugging logic for a given SQL query.
        """
        logger.info("--- Executing Phase: SQL Debugging ---")
        
        debugged_sql_message = self.system_agent.debug_sql(
            conversation=conversation,
            original_sql=original_sql,
            execution_error=execution_error
        )
        
        debugged_sql = self.system_agent.extract_sql_from_message(debugged_sql_message)
        
        self.data_handler.save_sql_result(debugged_sql, self.config.data.file_patterns.sql_results_debug)
        return debugged_sql