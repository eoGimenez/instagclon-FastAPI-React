from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    ORIGIN: str
    SECRET_KEY: str
    ALGORITHM: str
    CLOUDNAME: str
    CLOUDKEY: str
    CLOUDSECRET: str

    model_config = SettingsConfigDict(env_file= '.env')


@lru_cache()
def get_settings():
    return Settings()