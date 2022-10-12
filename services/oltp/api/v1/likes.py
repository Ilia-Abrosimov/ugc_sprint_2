from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from maps.maps import UserLikes
from schemas.film_likes import (DeleteFilmLikeParams, DeleteFilmLikeResponse, GetUserLikesParams, GetUserLikesResponse,
                                LikeFilmBody, LikeFilmParams, LikeFilmResponse, UpdateLikeBody, UpdateLikeParams,
                                UpdateLikeResponse)
from storages.mongo_storage import MongoStorage
from utils.injectors import hot_storage_injector
from utils.json_response import json_response
from utils.unpack import unpack_models

likes_bp = Blueprint('likes', __name__, url_prefix='/api/v1/likes')
TAG = 'Likes'
DB_NAME = 'default'
TABLE = 'likes'


@likes_bp.route('/', methods=['POST'])
@spec.validate(
    query=LikeFilmParams,
    body=LikeFilmBody,
    resp=Response(HTTP_200=LikeFilmResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def create_like(
        query: LikeFilmParams,
        body: LikeFilmBody,
        storage: MongoStorage,
) -> LikeFilmResponse:
    """ Like/dislike film.
        ---
    """
    data = {'user_id': str(query.user_id), 'film_id': str(body.film_id), 'value': body.value}
    loop = storage.client.get_io_loop()

    result = loop.run_until_complete(storage.add(db_name=DB_NAME, table=TABLE, data=data))

    return LikeFilmResponse(message=f'Оценка {result} к фильму {str(body.film_id)} добавлена.')


@likes_bp.route('/', methods=['GET'])
@spec.validate(
    query=GetUserLikesParams,
    resp=Response(HTTP_200=GetUserLikesResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def get_user_likes(query: GetUserLikesParams, storage: MongoStorage) -> GetUserLikesResponse:
    """ Get user likes/dislikes
        ---
    """
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.read_many(db_name=DB_NAME, table=TABLE, user_id=str(query.user_id)))

    return GetUserLikesResponse(films=[UserLikes(**item, id=str(item['_id'])) for item in result])


@likes_bp.route('/', methods=['PUT'])
@spec.validate(
    query=UpdateLikeParams,
    body=UpdateLikeBody,
    resp=Response(HTTP_200=UpdateLikeResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def update_like(query: UpdateLikeParams, body: UpdateLikeBody, storage: MongoStorage) -> UpdateLikeResponse:
    """ Update like.
        ---
    """
    data = {'user_id': str(query.user_id), 'film_id': str(body.film_id), 'value': body.value}
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.update(db_name=DB_NAME, table=TABLE, data=data))

    return UpdateLikeResponse(message=f'Оценка {result} к фильму {str(body.film_id)} обновлена.')


@likes_bp.route('/', methods=['DELETE'])
@spec.validate(
    query=DeleteFilmLikeParams,
    resp=Response(HTTP_200=DeleteFilmLikeResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def delete_like(query: DeleteFilmLikeParams, storage: MongoStorage) -> DeleteFilmLikeResponse:
    """ Delete like/dislike.
        ---
    """
    loop = storage.client.get_io_loop()
    loop.run_until_complete(storage.delete(db_name=DB_NAME, table=TABLE, obj_id=str(query.like_id)))

    return DeleteFilmLikeResponse(message=f'Оценка {str(query.like_id)} удалена.')
