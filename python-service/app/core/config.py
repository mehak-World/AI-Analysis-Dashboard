import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load the root .env first
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

ENV_FILE = BASE_DIR / ".envs" / f".env.{ENVIRONMENT}"


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    PORT: int

    ALLOWED_ORIGINS: list[str]

    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str = Field(
        validation_alias=AliasChoices("AWS_S3_BUCKET", "S3_BUCKET_NAME")
    )

    MONGO_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []

            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                parsed = None

            if isinstance(parsed, list):
                return [item.strip() for item in parsed if isinstance(item, str) and item.strip()]
            if isinstance(parsed, str):
                return [parsed.strip()] if parsed.strip() else []

            return [item.strip() for item in value.strip("[]").split(",") if item.strip()]

        return value


settings = Settings()