"""Runtime configuration, loaded from environment / .env."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    azure_devops_org: str = ""
    azure_devops_project: str = ""
    azure_devops_team: str = ""
    azure_devops_pat: str = ""

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-5"

    board_config_path: str = "./board_config.yaml"


def load_settings() -> Settings:
    return Settings()
