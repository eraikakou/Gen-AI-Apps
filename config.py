"""
Central configuration for ctrlauto_commons.

The package defines WHICH settings exist; each project supplies ALL the VALUES.
There are no defaults: every setting must be provided, otherwise the first
call to get_settings() fails with a validation error listing what's missing.

Resolution order (highest priority first):
    1. configure(...) called from project code
    2. Environment variables  (e.g. MLFLOW_EXPERIMENT_NAME=...)
    3. .env file in the working directory

Env var names match the old constant names (case-insensitive), so projects
that already set MLFLOW_TRACKING_URI, DATABRICKS_HOST, LLM_MODEL, ... keep working.

Usage inside the package (always read at CALL time, never at import time):

    from ctrlauto_commons.config import get_settings

    def my_function():
        s = get_settings()
        mlflow.set_experiment(s.mlflow_experiment_name)
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Project identity
    # ------------------------------------------------------------------
    control_id: str = Field(description="Control this project automates, e.g. 'A1925_BCCH-205'")
    case_id_field: str = Field(description="Project-specific name of the unique case ID, e.g. 'PICHID'")

    # ------------------------------------------------------------------
    # Databricks / MLflow
    # ------------------------------------------------------------------
    databricks_host: str = Field(description="Databricks workspace URL")
    mlflow_tracking_uri: str
    mlflow_registry_uri: str
    mlflow_experiment_name: str
    mlflow_trace_artifact_path: str
    mlflow_trace_search_max_results: int = Field(gt=0)

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------
    llm_model: str
    llm_temperature: float = Field(ge=0.0, le=2.0)
    llm_max_tokens: int = Field(gt=0)
    llm_request_timeout_seconds: int = Field(gt=0)
    llm_retry_max_attempts: int = Field(ge=1)
    prompt_version: str

    # ------------------------------------------------------------------
    # Quality assurance
    # ------------------------------------------------------------------
    ai_ok_cases_qa_sample_size: int = Field(ge=0)


# ----------------------------------------------------------------------
# Access
# ----------------------------------------------------------------------
_settings: Settings | None = None


def configure(**values) -> Settings:
    """
    Set settings from project code. Call once at startup, before using
    anything else from the package. Values not passed here are read from
    env vars / .env; anything missing from all sources raises an error.
    """
    global _settings
    _settings = Settings(**values)
    return _settings


def get_settings() -> Settings:
    """Return the active settings, loading them from env / .env on first use."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Forget loaded settings (mainly for tests)."""
    global _settings
    _settings = None
