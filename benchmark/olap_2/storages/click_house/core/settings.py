from typing import Optional

from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    host: str = 'localhost'
    port: Optional[int] = None
    alt_hosts: Optional[list[str]] = None
    db: str = 'test'
    table: str = 'likes'

    @property
    def hosts_str(self):
        if self.alt_hosts:
            return ','.join(self.alt_hosts)
        return None

    class Config:
        env_file = '../../../.env'
        env_prefix = 'CLICKHOUSE_'


ch_settings = ClickHouseSettings()
