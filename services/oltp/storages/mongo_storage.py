from http import HTTPStatus
from typing import Union

import motor.motor_asyncio
from bson import ObjectId
from core.config import mongo_settings
from messages.messages import Errors
from utils.json_abort import json_abort


class MongoStorage:

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{mongo_settings.host}:{mongo_settings.port}/')

    async def check_existence(
            self,
            db_name: str,
            table: str,
            user_id: str,
            other_param: str,
            other_id: str,
    ) -> Union[bool, str]:
        db = self.client[db_name]
        collection = db[table]
        doc = await collection.find_one({'user_id': user_id, other_param: other_id})
        if doc:
            return doc['_id']

        return False

    async def add(self, db_name: str, table: str, data: dict, search: str = 'film_id') -> str:
        db = self.client[db_name]
        collection = db[table]

        if await self.check_existence(
                db_name=db_name,
                table=table,
                user_id=data['user_id'],
                other_param=search,
                other_id=data[search],
        ):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, Errors.ALREADY_EXISTS)

        result = await collection.insert_one(data)

        return result.inserted_id

    async def update(self, db_name: str, table: str, data: dict, search: str = 'film_id') -> str:
        db = self.client[db_name]
        collection = db[table]
        doc = await self.check_existence(
                db_name=db_name,
                table=table,
                user_id=data['user_id'],
                other_param=search,
                other_id=data[search],
        )

        if not doc:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, Errors.NOT_EXISTS)

        result = await collection.replace_one({'_id': ObjectId(doc)}, data)

        return result.modified_count

    async def read_many(self, db_name: str, table: str, user_id: str) -> list:
        db = self.client[db_name]
        collection = db[table]
        docs = collection.find({'user_id': user_id})

        return [doc for doc in await docs.to_list(length=100)]

    async def read_one(self, db_name: str, table: str, obj_id: str) -> dict:
        db = self.client[db_name]
        collection = db[table]
        doc = await collection.find_one({'_id': ObjectId(obj_id)})
        if not doc:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, Errors.NOT_EXISTS)

        return doc

    async def delete(self, db_name: str, table: str, obj_id: str) -> None:
        db = self.client[db_name]
        collection = db[table]
        result = await collection.delete_one({'_id': ObjectId(obj_id)})
        if not result.raw_result['n']:
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, Errors.NOT_EXISTS)
