from enum import Enum

from pymongo import MongoClient as Client
from storages.base_client import BaseClient
from storages.mongo.core.settings import mongo_settings


class LIKES_TYPES(int, Enum):
    LIKE = 1
    DISLIKE = 0


class MongoClient(BaseClient):

    def __init__(self, local=False):
        self.client = Client(f'mongodb://{mongo_settings.MONGO_HOST}:{mongo_settings.MONGO_PORT}')
        if local:
            self.client = Client(f'mongodb://localhost:{mongo_settings.MONGO_PORT}')
        self.db = self.client['films']
        self.collection = self.db['likes']

    def add_data(self, data: list[dict[str, str, int]]) -> list:
        result = self.collection.insert_many(data)

        return result.inserted_ids

    def get_liked_films(self, user_id: str) -> list:
        result = self.collection.find({"user_id": user_id, "like": 1})
        films = [film for film in result]

        return films

    def get_film_likes(self, film_id: str) -> dict:
        result = self.collection.aggregate([
            {'$match': {'film_id': film_id}},
            {'$group': {'_id': '$like', 'count': {'$sum': 1}}}
        ])

        return {LIKES_TYPES(item['_id']).name: item['count'] for item in result}

    def get_film_rating(self, film_id: str) -> float:
        result = self.collection.aggregate([
            {'$match': {'film_id': film_id}},
            {'$group': {'_id': '$like', 'count': {'$sum': 1}}}
        ])
        marks = {item['_id']: item['count'] for item in result}
        if marks.get(1):
            rating = marks[1] * 10 / sum(marks.values())
            return rating
        rating = 0.0
        return rating
