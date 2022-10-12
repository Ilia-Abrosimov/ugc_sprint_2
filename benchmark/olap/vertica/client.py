import vertica_python
from src.models import UserHistory
from vertica.core.settings import vertica_conn


class VerticaClient:

    def __init__(self):
        self.conn = vertica_python.connect(**vertica_conn.dict())
        self.curs = self.conn.cursor()

    def create_table(self):
        self.curs.execute("""
            CREATE TABLE IF NOT EXISTS views (
                id IDENTITY,
                user_id VARCHAR(256) NOT NULL,
                film_id VARCHAR(256) NOT NULL,
                viewed_frame INTEGER NOT NULL
            );
            """
                          )

    def truncate_table(self):
        self.curs.execute("""TRUNCATE TABLE views;""")

    def drop_table(self):
        self.curs.execute("""DROP TABLE views;""")

    def add_data(self, batch: int):
        data = [tuple(UserHistory().dict().values()) for _ in range(batch)]
        query = "INSERT INTO views (user_id, film_id, viewed_frame) VALUES (%s, %s, %s)"
        self.curs.executemany(query, data)

    def read_data(self):
        user_id = UserHistory().dict()['user_id']
        film_id = UserHistory().dict()['film_id']
        query = "SELECT user_id FROM views WHERE (user_id=%s) AND (film_id=%s)"
        self.curs.execute(query % (user_id, film_id))

    def close_conn(self):
        self.curs.close()
