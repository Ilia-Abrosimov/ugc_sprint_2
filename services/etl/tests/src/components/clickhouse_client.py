"""
Клиент ClickHouse.

Чтение данных из таблиц.

"""

from clickhouse_driver import Client
from etl.src.core.settings import ch_settings


class ClickHouseClient:

    def __init__(self, local: bool = False):
        if local:
            self.client = Client(host=ch_settings.host)
        else:
            self.client = Client(host=ch_settings.host, alt_hosts=ch_settings.hosts_str, port=ch_settings.port)

    def read_data(self, db: str, table: str) -> list:
        query = "SELECT * FROM %s.%s"
        return self.client.execute(query % (db, table))

    def truncate_table(self, db: str, table: str) -> None:
        query = "TRUNCATE TABLE %s.%s"
        self.client.execute(query % (db, table))
