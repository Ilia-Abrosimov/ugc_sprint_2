from abc import ABC, abstractmethod


class BaseClient(ABC):

    @abstractmethod
    def add_data(self, data: list[dict[str, str, int]]):
        """ Добавление информации о том, что пользователь поставил фильму оценку (0 или 1). """

    @abstractmethod
    def get_liked_films(self, user_id: str):
        """ Список фильмов, которым пользователь поставил лайк (1). """

    @abstractmethod
    def get_film_likes(self, film_id: str):
        """ Подсчет количества лайков (1) и дизлайков (0) у фильма. """

    @abstractmethod
    def get_film_rating(self, film_id: str):
        """ Расчет рейтинга фильма (отношение лайков к общему количеству оценок). """
