from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    database_url: str
    secret: str = 'Супер секретное слово – пряник'
    first_superuser_email: None | EmailStr = None
    first_superuser_password: None | str = None

    class Config:
        env_file = '.env'


settings = Settings()
