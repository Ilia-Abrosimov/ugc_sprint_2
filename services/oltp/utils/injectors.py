"""
Изобретаем dependency injector...

cold_storage - хранилище данных, предназначенных, в первую очередь, для аналитики.
hot_storage - хранилище данных, предназначенных для доступа к своим данным пользователей и для аналитики.

"""


import functools

from storages.kafka_storage import KafkaStorage
from storages.mongo_storage import MongoStorage


def cold_storage_injector(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, storage=KafkaStorage(), **kwargs)

    return wrapper


def hot_storage_injector(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, storage=MongoStorage(), **kwargs)

    return wrapper
