import unittest
import warnings
from operator import itemgetter

from etl.src.components.loader.ch_loader import ClickHouseLoader
from etl.src.maps.maps import UserHistoryMap
from tests.src.components.clickhouse_client import ClickHouseClient
from tests.src.models.models import UserHistory


class TestLoader(unittest.TestCase):

    def setUp(self):
        self.loader = ClickHouseLoader(local=True)
        self.test_client = ClickHouseClient(local=True)
        self.amount = 3
        self.data = [UserHistory().dict() for _ in range(self.amount)]

    def tearDown(self):
        self.test_client.truncate_table('shard', UserHistoryMap.table)
        self.test_client.truncate_table('replica', UserHistoryMap.table)

    def test_loader(self):
        warnings.filterwarnings(action='ignore', message='unclosed', category=ResourceWarning)
        self.loader.add_data(
            UserHistoryMap.database,
            UserHistoryMap.table,
            UserHistoryMap.fields,
            self.data,
        )
        result = self.test_client.read_data(
            UserHistoryMap.database,
            UserHistoryMap.table,
        )
        converted_result = [
            UserHistory(**dict(zip(UserHistory().dict().keys(), item))).dict()
            for item in result
        ]

        assert [
                   item for item in sorted(converted_result, key=itemgetter('id'))
                ] == [
                   item for item in sorted(self.data, key=itemgetter('id'))
                ]


if __name__ == '__main__':
    unittest.main()
