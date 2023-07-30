from functools import lru_cache
from enviroment import config_env

@lru_cache()
def get_settings():
    return config_env.Settings()