from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_API_KEY: str
    AZURE_SEARCH_INDEX_NAME: str
    OPENAI_ENDPOINT: str
    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str
    OPENAI_LLM_MODEL: str
    OPENAI_API_VERSION: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
