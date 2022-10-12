from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from maps.maps import UserBookmarks
from schemas.bookmarks import (CreateBookmarkBody, CreateBookmarkParams, CreateBookmarkResponse, DeleteBookmarkParams,
                               DeleteBookmarkResponse, GetBookmarksParams, GetBookmarksResponse)
from storages.mongo_storage import MongoStorage
from utils.injectors import hot_storage_injector
from utils.json_response import json_response
from utils.unpack import unpack_models

bookmarks_bp = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')
TAG = 'Bookmarks'
DB_NAME = 'default'
TABLE = 'bookmarks'


@bookmarks_bp.route('/', methods=['POST'])
@spec.validate(
    query=CreateBookmarkParams,
    body=CreateBookmarkBody,
    resp=Response(HTTP_200=CreateBookmarkResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def create_bookmark(
        query: CreateBookmarkParams,
        body: CreateBookmarkBody,
        storage: MongoStorage,
) -> CreateBookmarkResponse:
    """ Create bookmark.
        ---
    """
    data = {'user_id': str(query.user_id), 'film_id': str(body.film_id)}
    loop = storage.client.get_io_loop()

    result = loop.run_until_complete(storage.add(db_name=DB_NAME, table=TABLE, data=data))

    return CreateBookmarkResponse(message=f'Закладка {result} для фильма {str(body.film_id)} создана.')


@bookmarks_bp.route('/', methods=['GET'])
@spec.validate(
    query=GetBookmarksParams,
    resp=Response(HTTP_200=GetBookmarksResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def get_user_bookmarks(query: GetBookmarksParams, storage: MongoStorage) -> GetBookmarksResponse:
    """ Get user bookmarks.
        ---
    """
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.read_many(db_name=DB_NAME, table=TABLE, user_id=str(query.user_id)))

    return GetBookmarksResponse(bookmarks=[UserBookmarks(**item, id=str(item['_id'])) for item in result])


@bookmarks_bp.route('/', methods=['DELETE'])
@spec.validate(
    query=DeleteBookmarkParams,
    resp=Response(HTTP_200=DeleteBookmarkResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def remove_bookmark(
        query: DeleteBookmarkParams,
        storage: MongoStorage,
) -> DeleteBookmarkResponse:
    """ Remove bookmark.
        ---
    """
    loop = storage.client.get_io_loop()
    loop.run_until_complete(storage.delete(db_name=DB_NAME, table=TABLE, obj_id=str(query.bookmark_id)))

    return DeleteBookmarkResponse(message=f'Закладка {str(query.bookmark_id)} удалена.')
