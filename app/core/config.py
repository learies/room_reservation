from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    app_description: str
    database_url: str
    database_url_test: str

    class Config:
        env_file = ".env"


settings = Settings()
