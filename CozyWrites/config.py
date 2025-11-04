from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    # map the exact env names you set on Render (case-sensitive)
    DATABASE_HOSTNAME: str = Field(..., env="DATABASE_HOSTNAME")
    DATABASE_USERNAME: str = Field(..., env="DATABASE_USERNAME")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINS: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINS")

    class Config:
        # use local .env only for local dev; Render will supply real envs
        env_file = str(env_path) if env_path.exists() else None

settings = Settings()