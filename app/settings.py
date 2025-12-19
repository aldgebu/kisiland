from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    ENV_TYPE: str = 'development'

    JWT_SECRET_KEY: str

    PROD_DATABASE_URL: str = ''
    DEV_DATABASE_URL: str | None = None

    MONGODB_URI: str = ''
    MONGODB_DATABASE: str = ''


class _DevelopmentSettings(_Settings):
    debug: bool = True

    @property
    def database_url(self):
        return self.DEV_DATABASE_URL


class _ProductionSettings(_Settings):
    debug: bool = False

    @property
    def database_url(self):
        return self.PROD_DATABASE_URL


_settings = _Settings()
settings = _ProductionSettings() if _settings.ENV_TYPE == 'production' else _DevelopmentSettings()

__all__ = ['settings']
