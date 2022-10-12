"""
Подготовка данных для загрузки в аналитическое хранилище.

Данные распределяются в словаре по БД и таблицам в соответствии
с топиками.

"""
import ast

import backoff
from src.components.transformer.base import BaseTransformer
from src.core.settings import backoff_config
from src.maps.maps import clickhouse_schema as schema
from src.utils.logger import etl_logger


class ClickHouseTransformer(BaseTransformer):

    __slots__ = ('data_dict', 'database', 'table', 'fields', 'model')

    def __init__(self):
        self.data_dict = {}
        self.database = None
        self.table = None
        self.fields = None
        self.model = None

    @backoff.on_exception(**backoff_config, logger=etl_logger)
    def transform(self, records: dict) -> dict:
        self.data_dict = {}
        for partition, consumer_records in records.items():
            for record in consumer_records:
                if record.topic in schema:
                    # В трансформер приходят все данные, в т.ч. те, которые, возможно, не нужно
                    # загружать в КликХаус. Поэтому проверяем, есть ли топик в схеме данных.
                    self.database = schema[record.topic].database
                    self.table = schema[record.topic].table
                    self.fields = schema[record.topic].fields
                    self.model = schema[record.topic].model
                    self._add_data_to_dict(data=self.model(**ast.literal_eval(record.value.decode())).dict())

        return self.data_dict

    def _add_data_to_dict(self, data: dict) -> None:
        self.data_dict.setdefault(self.database, {})

        if self.table not in self.data_dict[self.database]:
            self.data_dict[self.database][self.table] = {'fields': self.fields, 'src': []}

        self.data_dict[self.database][self.table]['src'].append(data)
