# pipeline/main_pipeline.py

import logging
from pathlib import Path

# Core models and utilities
from models.config import AppConfig
from models.conversation import Conversation, Message
from agents.system_agent import SystemAgent
from agents.user_simulator_parser import UserSimulatorParserAgent
from agents.user_simulator_generator import UserSimulatorGeneratorAgent
from utils.data_handler import DataHandler
from utils.llm_api_caller import LLMAPICaller
from utils.schema_loader import SchemaLoader

# --- THIS IS THE KEY CHANGE ---
# Import the specialist runners from their dedicated files
from .ambiguity_resolution import AmbiguityResolutionRunner
from .debugging import DebuggingRunner
# from .follow_up import FollowUpRunner # For the future

logger = logging.getLogger(__name__)

class AgenticPipeline:
    """
    The Conductor of the BIRD-Interact agentic framework.
    """
    def __init__(self, config: AppConfig, project_root: Path):
        # ... (this part is identical to the previous version)
        self.config = config
        self.project_root = project_root
        self.state = {}
        logger.info("Initializing Agentic Pipeline Conductor...")
        self._initialize_components()
        self._initialize_phase_runners()
        logger.info("Conductor and all components are ready.")

    def _initialize_components(self):
        # ... (this part is identical to the previous version)
        self.llm_caller = LLMAPICaller(self.config)
        self.data_handler = DataHandler(self.config, self.project_root)
        self.schema_loader = SchemaLoader(self.config, self.project_root)
        self.system_agent = SystemAgent(self.config, self.llm_caller)
        self.user_parser = UserSimulatorParserAgent(self.config, self.llm_caller)
        self.user_generator = UserSimulatorGeneratorAgent(self.config, self.llm_caller)

    def _initialize_phase_runners(self):
        """Instantiates the specialist runners for each pipeline phase."""
        # The instantiation logic is the same, just the import source has changed.
        self.ambiguity_resolution_runner = AmbiguityResolutionRunner(
            self.config, self.system_agent, self.user_parser, self.user_generator, self.data_handler
        )
        self.debugging_runner = DebuggingRunner(
            self.config, self.system_agent, self.data_handler
        )
        # ... initialize other runners (FollowUpRunner, etc.) here

    def run(self):
        """
        Executes the full pipeline for all data items.
        """
        # Load the initial dataset (e.g., bird_interact_data.jsonl)
        all_data_items = self.data_handler.load_initial_data()
        
        if self.config.development.limit_samples:
            all_data_items = all_data_items[:self.config.development.limit_samples]
            logger.warning(f"Running in development mode. Limiting to {self.config.development.limit_samples} samples.")

        for item in all_data_items:
            self.process_item(item)

    def process_item(self, data_item):
        """
        Processes a single item through the entire multi-phase pipeline.
        """
        logger.info(f"--- Processing new item (ID: {data_item.get('id', 'N/A')}) ---")
        
        # Initialize state for this item
        self.state = {
            'conversation': Conversation(),
            'sql_results': {},
            'execution_reports': {}
        }
        initial_message = Message(role="user", content=data_item['question'])
        self.state['conversation'].add_message(initial_message)

        # === Phase 1: Ambiguity Resolution ===
        if self.config.pipeline.phases.ambiguity_resolution.enabled:
            final_conv, sql = self.ambiguity_resolution_runner.run(self.state['conversation'])
            self.state['conversation'] = final_conv
            self.state['sql_results']['phase1'] = sql

        # === Phase 1: Debugging ===
        if self.config.pipeline.phases.debugging.enabled:
            # In a real run, this report would come from the evaluation script
            execution_report = self._get_execution_report('phase1') 
            if execution_report and not execution_report['is_correct']:
                debugged_sql = self.debugging_runner.run(
                    conversation=self.state['conversation'],
                    original_sql=self.state['sql_results']['phase1'],
                    execution_error=execution_report['error_message']
                )
                self.state['sql_results']['phase1_debugged'] = debugged_sql
        
        # === Phase 2: Follow-Up Question (and its debugging) would follow the same pattern ===
        # ...

        logger.info(f"--- Finished processing item (ID: {data_item.get('id', 'N/A')}) ---")

    def _get_execution_report(self, phase_key: str) -> dict:
        # Placeholder for logic that runs the SQL and gets a report.
        # This could call the `eval_bird_interact_batch.py` script.
        logger.info(f"Simulating execution for '{phase_key}' SQL.")
        if self.state['sql_results'].get(phase_key):
            return {'is_correct': False, 'error_message': 'Syntax error near SELECT'}
        return None