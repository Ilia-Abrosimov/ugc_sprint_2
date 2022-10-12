from core.settings import LIKES_TYPES
from pymongo import MongoClient


class MongoHandler:
    likes_collection = 'likes'
    reviews_collection = 'reviews'
    review_likes_collection = 'review_likes'
    bookmarks_collection = 'bookmarks'

    def __init__(self, client: MongoClient, db: str):
        self._client = client
        self._db = client.get_database(db)

    def get_user_likes(self, user_id: str) -> list[str]:
        """ Список фильмов, которые понравились пользователю """
        result = self._db.get_collection(self.likes_collection).find({'user_id': user_id, 'like': LIKES_TYPES.LIKE})
        return [item['film_id'] for item in result]

    def get_user_reviews(self, user_id: str) -> list[dict]:
        """ Список рецензий пользователя """
        result = self._db.get_collection(self.reviews_collection).aggregate(
            [{'$match': {'user_id': user_id}}, {'$project': {'_id': 0, 'film_id': '$film_id', 'review': '$review'}}]
        )
        return [item for item in result]

    def get_user_bookmarks(self, user_id: str) -> list[str]:
        """ Список закладок пользователя """
        result = self._db.get_collection(self.bookmarks_collection).find({'user_id': user_id})
        return [item['film_id'] for item in result]
