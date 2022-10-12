from enum import Enum

from clickhouse_driver import Client
from storages.base_client import BaseClient
from storages.click_house.core.settings import ch_settings


class LIKES_TYPES(int, Enum):
    LIKE = 1
    DISLIKE = 0


class ClickHouseClient(BaseClient):
    """ """

    def __init__(self):
        self.client = Client(host=ch_settings.host, alt_hosts=ch_settings.hosts_str, port=ch_settings.port)

    def _format_response(self, response: list) -> list:
        return [x[0] if len(x) == 1 else x for x in response]

    def add_data(self, data: list[dict[str, str, int]]) -> None:
        """ Добавление информации о том, что пользователь поставил фильму оценку (0 или 1). """
        query = 'INSERT INTO %s.%s (user_id, film_id, like) VALUES'
        self.client.execute(query % (ch_settings.db, ch_settings.table), data)

    def get_liked_films(self, user_id: str) -> list:
        """ Список фильмов, которым пользователь поставил лайк (1). """
        query = f"""
        SELECT film_id
        FROM %s.%s
        WHERE (like == 1) AND (user_id == '{user_id}')
        """
        result = self.client.execute(query % (ch_settings.db, ch_settings.table))
        return self._format_response(result)

    def get_film_likes(self, film_id: str) -> dict:
        """ Подсчет количества лайков (1) и дизлайков (0) у фильма. """
        query = f"""
        SELECT like, COUNT(like)
        FROM %s.%s
        WHERE (film_id == '{film_id}')
        GROUP BY like
        """
        response = self.client.execute(query % (ch_settings.db, ch_settings.table))
        formatted_response = {k: v for k, v in response}
        result = {'likes': formatted_response[LIKES_TYPES.LIKE], 'dislikes': formatted_response[LIKES_TYPES.DISLIKE]}
        return result

    def get_film_rating(self, film_id: str) -> float:
        """ Расчет рейтинга фильма (отношение лайков к общему количеству оценок). """
        query = f"""
        SELECT like, COUNT(like)
        FROM %s.%s
        WHERE (film_id == '{film_id}')
        GROUP BY like
        """
        response = self.client.execute(query % (ch_settings.db, ch_settings.table))
        response = {k: v for k, v in response if k in (LIKES_TYPES.LIKE, LIKES_TYPES.DISLIKE)}

        return response[LIKES_TYPES.LIKE] / sum(response.values())
