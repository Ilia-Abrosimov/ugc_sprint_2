"""
Настройки для доступа к хранилищам.

"""

from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    host: str
    port: str
    alt_hosts: list[str]

    @property
    def hosts_str(self):
        return ','.join(self.alt_hosts)

    class Config:
        env_prefix = 'CLICKHOUSE_'


ch_settings = ClickHouseSettings()
