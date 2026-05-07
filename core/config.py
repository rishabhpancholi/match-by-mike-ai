from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    openai_api_key: str
    supabase_url: str
    supabase_key: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
