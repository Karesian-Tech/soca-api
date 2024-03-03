import os
from typing import Optional
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_TEST_NAME: str
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_HOST: str
    DB_TEST_PORT: str

    def _get_postgres_url(self, db_name, db_user, db_pass, db_host, db_port):
        return f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    def get_db_url(self, env: Optional[str] = None):
        if env:
            if env == "test":
                return self._get_postgres_url(
                    self.DB_TEST_NAME,
                    self.DB_TEST_USER,
                    self.DB_TEST_PASS,
                    self.DB_TEST_HOST,
                    self.DB_TEST_PORT,
                )
        return self._get_postgres_url(
            self.DB_NAME,
            self.DB_USER,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AppSettings()
