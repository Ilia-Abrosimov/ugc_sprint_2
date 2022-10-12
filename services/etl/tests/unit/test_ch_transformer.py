import unittest
from collections import namedtuple

from etl.src.components.transformer.ch_transformer import ClickHouseTransformer
from etl.src.maps.maps import UserHistoryMap
from tests.src.models.models import UserHistory


class TestTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = ClickHouseTransformer()
        self.values = [UserHistory().dict() for _ in range(3)]
        consumer_records = namedtuple('records', ['topic', 'value'])
        self.records = {
            'partition':
                [
                    consumer_records(**{'topic': 'views', 'value': str.encode(str(value))}) for value in self.values
                ]
        }

    def test_transform(self):
        data_dict = self.transformer.transform(self.records)
        for database, table in data_dict.items():
            for table_name, table_data in table.items():
                assert database == UserHistoryMap.database
                assert table_name == UserHistoryMap.table
                assert table_data['fields'] == UserHistoryMap.fields
                assert table_data['src'] == self.values


if __name__ == '__main__':
    unittest.main()
