from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    origin: str
    secret_key: str
    algorithm: str
    cloudname: str
    cloudkey: str
    cloudsecret: str

    model_config = SettingsConfigDict(env_file= '.env')


@lru_cache()
def get_settings():
    return Settings()