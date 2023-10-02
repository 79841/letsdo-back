from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    PROFILE_IMAGE_DIR: str

    class Config:
        env_file = '.env'


settings = Settings()
