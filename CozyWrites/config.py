from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    database_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    database_username: str = Field(..., env="DATABASE_USERNAME")
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    database_name: str = Field(..., env="DATABASE_NAME")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_mins: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINS")

    class Config:
        env_file = str(env_path) if env_path.exists() else None

settings = Settings()