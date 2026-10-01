import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    nebius_api_key: str | None
    nebius_base_url: str
    nebius_model: str | None


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL") or "sqlite:///./app.db",
        nebius_api_key=os.getenv("NEBIUS_API_KEY") or None,
        nebius_base_url=os.getenv(
            "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"
        ),
        nebius_model=os.getenv("NEBIUS_MODEL") or None,
    )
