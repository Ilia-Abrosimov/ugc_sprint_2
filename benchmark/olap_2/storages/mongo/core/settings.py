"""
Настройки для доступа к хранилищам.

"""

from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_HOST: str
    MONGO_PORT: int

    class Config:
        env_file = '../../.env'


mongo_settings = MongoSettings()
