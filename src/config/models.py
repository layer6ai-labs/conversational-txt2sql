from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Union
from pathlib import Path
import os

class ModelConfig(BaseModel):
    name: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(gt=0)
    timeout: int = Field(gt=0)
    retry_attempts: int = Field(ge=0)

class ModelsConfig(BaseModel):
    system_model: ModelConfig
    user_simulator_model: ModelConfig

class PhaseConfig(BaseModel):
    enabled: bool = True
    
class AmbiguityResolutionConfig(PhaseConfig):
    max_turns: int = Field(gt=0, default=5)

class DebuggingConfig(PhaseConfig):
    max_attempts: int = Field(ge=0, default=1)

class FollowUpConfig(PhaseConfig):
    generate_questions: bool = True

class PhasesConfig(BaseModel):
    ambiguity_resolution: AmbiguityResolutionConfig
    debugging: DebuggingConfig
    follow_up: FollowUpConfig
    follow_up_debugging: DebuggingConfig

class PipelineConfig(BaseModel):
    patience: int = Field(ge=1)
    max_concurrent_requests: int = Field(gt=0, default=5)
    enable_caching: bool = True
    phases: PhasesConfig

class DataPathsConfig(BaseModel):
    base_data: str
    db_schema_template: str
    external_kb_template: str
    
class DataOutputConfig(BaseModel):
    base_dir: str
    
class DataFilePatterns(BaseModel):
    system_interaction: str = "system_interaction.jsonl"
    system_prompt: str = "system_interaction_prompt.jsonl"
    system_response: str = "system_interaction_response.jsonl"
    user_1_interaction: str = "user_1_interaction.jsonl"
    user_1_prompt: str = "user_1_interaction_prompt.jsonl"
    user_1_response: str = "user_1_interaction_response.jsonl"
    user_2_interaction: str = "user_2_interaction.jsonl"
    user_2_prompt: str = "user_2_interaction_prompt.jsonl"
    user_2_response: str = "user_2_interaction_response.jsonl"
    sql_results: str = "sql_results.jsonl"
    sql_results_debug: str = "sql_results_debug.jsonl"
    sql_results_fu: str = "sql_results_fu.jsonl"
    sql_results_fu_debug: str = "sql_results_fu_debug.jsonl"

class DataConfig(BaseModel):
    input: DataPathsConfig
    output: DataOutputConfig
    file_patterns: DataFilePatterns

class ProjectConfig(BaseModel):
    name: str
    version: str
    root_path: str
    experiment_id: Optional[str] = None
    
    @validator('root_path')
    def validate_root_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Project root path does not exist: {v}")
        return v

class AgentConfig(BaseModel):
    prompt_templates_dir: str
    
class SystemAgentConfig(AgentConfig):
    sql_extraction_enabled: bool = True

class UserSimulatorConfig(BaseModel):
    parser: AgentConfig
    generator: AgentConfig

class AgentsConfig(BaseModel):
    system_agent: SystemAgentConfig
    user_simulator: UserSimulatorConfig

class EvaluationConfig(BaseModel):
    enabled: bool = True
    script_path: str
    output_suffix: str = "_output_with_status.jsonl"
    metrics: List[str] = ["execution_accuracy", "valid_efficiency", "sql_syntax_correctness"]

class RateLimitingConfig(BaseModel):
    requests_per_minute: int = Field(gt=0, default=100)
    requests_per_hour: int = Field(gt=0, default=1000)

class RetryConfig(BaseModel):
    max_retries: int = Field(ge=0, default=3)
    backoff_factor: float = Field(gt=0, default=2.0)
    max_backoff: int = Field(gt=0, default=60)

class APIConfig(BaseModel):
    rate_limiting: RateLimitingConfig
    retry_config: RetryConfig

class LogHandlerConfig(BaseModel):
    enabled: bool = True
    level: str = "INFO"

class FileLogHandlerConfig(LogHandlerConfig):
    filename: str
    max_bytes: int = Field(gt=0, default=10485760)
    backup_count: int = Field(ge=0, default=5)

class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers: Dict[str, Union[LogHandlerConfig, FileLogHandlerConfig]]
    loggers: Dict[str, str] = {}

class ErrorHandlingConfig(BaseModel):
    continue_on_failure: bool = False
    save_partial_results: bool = True
    max_consecutive_failures: int = Field(gt=0, default=3)
    empty_file_strategy: str = Field(default="skip", regex="^(skip|retry|fail)$")

class ProgressConfig(BaseModel):
    enabled: bool = True
    update_frequency: int = Field(gt=0, default=10)

class PerformanceConfig(BaseModel):
    track_timing: bool = True
    track_memory_usage: bool = False
    profile_enabled: bool = False

class MonitoringConfig(BaseModel):
    track_metrics: bool = True
    save_intermediate_results: bool = True
    progress: ProgressConfig
    performance: PerformanceConfig

class DevelopmentConfig(BaseModel):
    debug_mode: bool = False
    dry_run: bool = False
    limit_samples: Optional[int] = None
    debug_phases: Dict[str, bool] = {}

class FeaturesConfig(BaseModel):
    parallel_processing: bool = True
    async_api_calls: bool = True
    result_caching: bool = True
    schema_validation: bool = True

class AppConfig(BaseModel):
    """Main application configuration model"""
    project: ProjectConfig
    models: ModelsConfig
    pipeline: PipelineConfig
    data: DataConfig
    agents: AgentsConfig
    evaluation: EvaluationConfig
    api: APIConfig
    logging: LoggingConfig
    error_handling: ErrorHandlingConfig
    monitoring: MonitoringConfig
    development: DevelopmentConfig
    environment: str = "development"
    features: FeaturesConfig
    
    def get_result_dir(self) -> Path:
        """Get the results directory for current configuration"""
        model_name = self.models.system_model.name
        patience = self.pipeline.patience
        return Path(self.project.root_path) / self.data.output.base_dir / f"patience_{patience}" / model_name
    
    def get_data_file_path(self, pattern_name: str) -> Path:
        """Get full path for a data file pattern"""
        pattern = getattr(self.data.file_patterns, pattern_name)
        return self.get_result_dir() / pattern
    
    def get_input_data_path(self, template_path: str, db_name: str = None) -> Path:
        """Resolve input data paths with optional DB name substitution"""
        base_path = Path(self.project.root_path) / template_path
        if db_name and "[[DB_name]]" in str(base_path):
            base_path = Path(str(base_path).replace("[[DB_name]]", db_name))
        return base_path