from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env-non-dev')


settings = Settings()
