"""
Настройки для доступа к аналитическому хранилищу.

"""
from dataclasses import dataclass
from typing import Callable

import backoff
from pydantic import BaseSettings


class Settings(BaseSettings):

    class Config:
        env_file = '../../.env'


class ClickHouseSettings(Settings):
    host: str
    port: str
    alt_hosts: list[str]

    @property
    def hosts_str(self):
        return ','.join(self.alt_hosts)

    class Config:
        env_prefix = 'CLICKHOUSE_'


class KafkaSettings(Settings):
    bootstrap_servers: list[str]
    topics: list[str]
    group: str

    class Config:
        env_prefix = 'KAFKA_'


class ETLSettings(BaseSettings):
    batch_size: int = 2
    kafka_consumer_timeout: int = 1
    etl_manager_timeout: int = 1


@dataclass
class BackoffConfig:
    wait_gen: Callable = backoff.expo
    exception: type = Exception
    max_value: int = 128


ch_settings = ClickHouseSettings()
kafka_settings = KafkaSettings()
etl_settings = ETLSettings()
backoff_config = BackoffConfig().__dict__
