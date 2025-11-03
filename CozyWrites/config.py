from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_hostname: str 
    database_username: str 
    database_password: str 
    database_name: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_mins: int 

    class Config:
        env_file = str(Path(__file__).resolve().parent / ".env")

settings = Settings()