from enum import Enum
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    LOG_FILE: str = 'logs/olap.log'
    LOG_FILE_ROTATION: str = '100 MB'
    GET_TOP_AMOUNT: int = 100


class ClickHouseSettings(BaseSettings):
    host: str = 'localhost'
    port: Optional[int] = None
    alt_hosts: Optional[list[str]] = None
    db: str = 'default'
    table_views: str = 'views'
    table_likes: str = 'likes'

    @property
    def hosts_str(self):
        if self.alt_hosts:
            return ','.join(self.alt_hosts)
        return None

    class Config:
        env_file = '../../../.env'
        env_prefix = 'CLICKHOUSE_'


class MongoSettings(Settings):
    host: str = 'localhost'
    port: str = '27017'
    db: str = 'test'

    class Config:
        env_prefix = 'MONGO_'


class LIKES_TYPES(int, Enum):
    LIKE = 1
    DISLIKE = 0


settings = Settings()
ch_settings = ClickHouseSettings()
mongo_settings = MongoSettings()
