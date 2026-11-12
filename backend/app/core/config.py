from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SatyOne API"
    environment: str = "development"
    database_url: str | None = None
    secret_key: str = "local-development-only-change-me"
    frontend_origins: str = "http://localhost:5173"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]

settings = Settings()
