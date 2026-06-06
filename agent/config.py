from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    tavily_api_key: SecretStr = Field(..., alias="TAVILY_API_KEY")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    tavily_max_results: int = Field(default=3, ge=1, le=10, alias="TAVILY_MAX_RESULTS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
