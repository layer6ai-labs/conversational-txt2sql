import argparse
import yaml
import logging
from pathlib import Path

# Import the Pydantic model for config validation and the main orchestrator
from models.config import AppConfig
from pipeline.main_pipeline import AgenticPipeline
from utils.logging_config import setup_logging

# Dynamically determine the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description="Run the BIRD-Interact Agentic Pipeline.")
    parser.add_argument(
        "--config",
        type=str,
        default="config/main_config.yaml",
        help="Path to the configuration YAML file (relative to project root)."
    )
    args = parser.parse_args()

    config_path = PROJECT_ROOT / args.config
    
    try:
        # Load and validate the configuration
        with open(config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        config = AppConfig(**raw_config)

        # Set up logging using the configuration
        setup_logging(config.logging)
        logger = logging.getLogger(__name__)
        logger.info("Configuration loaded and validated successfully.")
        
        # Initialize and run the pipeline
        pipeline = AgenticPipeline(config, PROJECT_ROOT)
        pipeline.run()

        logger.info("Pipeline execution has finished.")

    except Exception as e:
        logging.basicConfig() # Basic logging if config fails
        logging.exception(f"A critical error occurred: {e}")

if __name__ == "__main__":
    main()