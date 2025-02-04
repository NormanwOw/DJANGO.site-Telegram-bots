from pydantic_settings import BaseSettings, SettingsConfigDict
import platform


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env-non-dev' if platform.system() == 'Windows' else 'deploy/.env',
    )

    DEBUG: int

    SECRET_KEY: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int


settings = Settings()
