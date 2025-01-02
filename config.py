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
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int


settings = Settings()
