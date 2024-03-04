from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_NAME: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_TEST_NAME: Optional[str] = None
    DB_TEST_USER: Optional[str] = None
    DB_TEST_PASS: Optional[str] = None
    DB_TEST_HOST: Optional[str] = None
    DB_TEST_PORT: Optional[str] = None

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


settings = AppSettings()
