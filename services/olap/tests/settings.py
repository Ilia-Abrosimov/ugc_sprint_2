from typing import Optional

from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    host: str = 'localhost'
    port: Optional[int] = None
    alt_hosts: Optional[list[str]] = None

    @property
    def hosts_str(self):
        if self.alt_hosts:
            return ','.join(self.alt_hosts)
        return None


ch_settings = ClickHouseSettings()
