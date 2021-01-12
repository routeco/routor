from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    map_path: Path

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
