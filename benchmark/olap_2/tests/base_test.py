import random
from typing import Type

from src.fake_data import FakeData
from storages.base_client import BaseClient


class BaseStorageTest:

    def __init__(self, client: Type[BaseClient], batch_size: int, other_client: Type[BaseClient] = None):
        self._client = client
        self._other_client = client if not other_client else other_client
        self._batch_size = batch_size
        self.data_generator = FakeData()
        self.pending = True
        self.actions = self.data_generator.user_actions()

    def test_write(self):
        offset = 0
        while offset < len(self.actions):
            self._client.add_data(data=self.actions[offset:offset+self._batch_size])
            offset += self._batch_size

    def test_read(self):
        user = random.choice(self.data_generator.users)
        film = random.choice(self.data_generator.films)
        self._other_client.get_liked_films(user.id)
        self._other_client.get_film_likes(film.id)
        self._other_client.get_film_rating(film.id)

    def read_in_parallel(self):
        while self.pending:
            self.test_read()
