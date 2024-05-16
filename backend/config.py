from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_client_id: str
    github_client_secret: str
    model_config = SettingsConfigDict(env_file=".env")
