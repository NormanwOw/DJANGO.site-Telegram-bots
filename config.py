from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env-non-dev')

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
