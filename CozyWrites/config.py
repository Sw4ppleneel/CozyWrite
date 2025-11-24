from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    # provide sensible defaults so Settings() won't fail if env missing
    DATABASE_HOSTNAME: str = Field("postgres", env="DATABASE_HOSTNAME")
    DATABASE_USERNAME: str = Field("postgres", env="DATABASE_USERNAME")
    DATABASE_PASSWORD: str = Field("password", env="DATABASE_PASSWORD")
    DATABASE_NAME: str = Field("fastapi", env="DATABASE_NAME")
    DATABASE_PORT: int = Field(5432, env="DATABASE_PORT")
    SECRET_KEY: str = Field("6904a12d5027d17d564e51aeb3f1e2b6110ad29254ecaaa10ad8bf0c04acdc2c", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINS: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINS")

    class Config:
        env_file = str(env_path) if env_path.exists() else None

settings = Settings()