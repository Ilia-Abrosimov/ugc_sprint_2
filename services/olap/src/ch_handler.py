from typing import Any

from clickhouse_driver import Client
from core.settings import LIKES_TYPES, ch_settings


class ClickHouseHandler:
    def __init__(self, client: Client):
        self._client = client

    def _format_response(self, response: list) -> list:
        return [x[0] if len(x) == 1 else x for x in response]

    def _get(self, query: str) -> Any:
        return self._client.execute(query)

    def get_top_by_views(self, amount: int) -> dict:
        """ Список лучших фильмов по количеству просмотров """
        query = f"""
        SELECT film_id, count(1) AS c
        FROM %s.%s
        GROUP BY film_id
        ORDER BY c DESC
        LIMIT {amount}
        """
        data = self._get(query % (ch_settings.db, ch_settings.table_views))
        result = {k: v for k, v in data}
        return result

    def get_film_rating(self, film_id: str) -> float:
        """ Расчет рейтинга фильма (отношение лайков к общему количеству оценок). """
        query = f"""
        SELECT like, COUNT(like)
        FROM %s.%s
        WHERE (film_id == '{film_id}')
        GROUP BY like
        """
        data = self._get(query % (ch_settings.db, ch_settings.table_likes))
        result = {k: v for k, v in data if k in (LIKES_TYPES.LIKE, LIKES_TYPES.DISLIKE)}
        if LIKES_TYPES.LIKE in result:
            rating = result[LIKES_TYPES.LIKE] * 10 / sum(result.values())
            return rating
        return 0.0

    def get_top_by_rating(self, amount: int) -> dict:
        """ Список лучших фильмов по рейтингу """
        # TODO: оптимизировать
        query = f"""
        SELECT film_id
        FROM %s.%s
        GROUP BY film_id
        LIMIT {amount}
        """
        films = self._format_response(self._get(query % (ch_settings.db, ch_settings.table_likes)))
        data = {k: self.get_film_rating(k) for k in films}
        result = dict(sorted(data.items(), reverse=True, key=lambda x: x[1]))
        return result
