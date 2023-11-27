from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = "/home/narisara/project/VirtualAssistant_Backend/.env"


settings = Settings()
