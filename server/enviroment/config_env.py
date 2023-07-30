from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    origin: str
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_file= '.env')