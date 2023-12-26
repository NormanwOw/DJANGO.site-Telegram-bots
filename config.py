from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env-non-dev')

    SECRET_KEY: str


settings = Settings()
