from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    database_url: str
    secret: str = 'Супер секретное слово – пряник'

    class Config:
        env_file = '.env'


settings = Settings()
