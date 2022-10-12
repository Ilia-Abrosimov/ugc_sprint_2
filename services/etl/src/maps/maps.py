"""
Схемы данных для загрузки в OLAP-хранилища.

"""

from dataclasses import dataclass

from src.models.models import UserHistory


@dataclass
class UserHistoryMap:
    database: str = 'default'
    table: str = 'views'
    fields: str = '(id, user_id, film_id, viewed_frame)'
    model: object = UserHistory


clickhouse_schema = {
    'views': UserHistoryMap,
}
