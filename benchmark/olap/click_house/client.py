from click_house.core.settings import ch_settings
from clickhouse_driver import Client
from src.models import UserHistory


class CHClient:

    def __init__(self):
        self.client = Client(host=ch_settings.host, alt_hosts=ch_settings.hosts_str, port=ch_settings.port)

    def create_table(self, table: str):
        self.client.execute(
            'CREATE TABLE IF NOT EXISTS default.%s '
            'ON CLUSTER company_cluster (id Int64, user_id Int64, film_id Int64, viewed_frame Int32) '
            'Engine=MergeTree() ORDER BY user_id' % table
        )

    def add_data(self, db: str, table: str, batch: int):
        data = (UserHistory().dict() for _ in range(batch))
        query = "INSERT INTO %s.%s (user_id, film_id, viewed_frame) VALUES"
        self.client.execute(query % (db, table), data)

    def read_data(self, db: str, table: str):
        user_id = UserHistory().dict()['user_id']
        film_id = UserHistory().dict()['film_id']
        query = "SELECT user_id FROM %s.%s WHERE (user_id=%s) AND (film_id=%s)"
        self.client.execute(query % (db, table, user_id, film_id))
