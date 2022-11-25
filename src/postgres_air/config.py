from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    jwt_secret: str
    jwt_algoritm: str = 'HS256'
    jwt_expiration: int = 3600

    class Config:
        env_file = '../.env'


settings = Settings()

