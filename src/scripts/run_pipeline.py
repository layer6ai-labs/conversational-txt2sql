import argparse
import yaml
import logging

from config.main_config import AppConfig # Using Pydantic for config validation
from utils.logging_config import setup_logging
from pipeline.main_pipeline import AgenticPipeline # This orchestrates the phases

setup_logging()
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run the BIRD-Interact Agentic Pipeline.")
    parser.add_argument("--config", type=str, default="config/main_config.yaml",
                        help="Path to the configuration YAML file.")
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            raw_config = yaml.safe_load(f)
        config = AppConfig(**raw_config) # Validate config with Pydantic

        logger.info(f"Starting BIRD-Interact Pipeline with config: {config.model_dump_json(indent=2)}")

        pipeline = AgenticPipeline(config)
        pipeline.run_ambiguity_resolution()
        pipeline.run_phase1_debugging()
        pipeline.run_follow_up_question()
        pipeline.run_phase2_debugging()

        logger.info("Pipeline execution completed.")

    except Exception as e:
        logger.exception(f"An error occurred during pipeline execution: {e}")
        # Optionally, clean up or trigger alerts

if __name__ == "__main__":
    main()