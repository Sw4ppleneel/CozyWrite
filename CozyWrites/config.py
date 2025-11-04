from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
# load local .env only when present (for local dev)
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_mins: int

    class Config:
        # do not force an env_file here — production will use environment variables
        env_file = None

settings = Settings()