from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    gemini_api_key: str
    tavily_api_key: str
    groq_api_key: str

    model_name_gemini: str = "gemini-1.5-flash"
    model_name_groq: str = "llama-3.1-70b-versatile"
    max_search_results: int = 5
    max_iterations: int = 3


settings = Settings()