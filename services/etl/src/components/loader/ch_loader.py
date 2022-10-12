"""
Загрузчик данных в аналитическое хранилище.

"""

import backoff
from clickhouse_driver import Client
from src.components.loader.base import BaseLoader
from src.core.settings import backoff_config, ch_settings
from src.utils.logger import ch_logger


class ClickHouseLoader(BaseLoader):

    __slots__ = ('client',)

    def __init__(self, local: bool = False):
        if local:
            self.client = Client(host=ch_settings.host)
        else:
            self.client = Client(host=ch_settings.host, alt_hosts=ch_settings.hosts_str, port=ch_settings.port)

    def upload_data(self, data_dict: dict) -> None:
        for database, table in data_dict.items():
            for table_name, table_data in table.items():
                self._add_data(database, table_name, table_data['fields'], table_data['src'])

    @backoff.on_exception(**backoff_config, logger=ch_logger)
    def _add_data(self, db: str, table: str, fields: str, data: list) -> None:
        query = "INSERT INTO %s.%s %s VALUES"
        self.client.execute(query % (db, table, fields), data)
