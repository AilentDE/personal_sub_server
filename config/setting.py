from functools import lru_cache
from schema.settings import Settings

@lru_cache
def get_settings():
    return Settings()

setting = get_settings()