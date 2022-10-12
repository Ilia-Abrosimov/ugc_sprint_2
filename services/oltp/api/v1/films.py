from http import HTTPStatus

from app import spec
from core.config import kafka_settings
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from messages.messages import message
from schemas.film_progress import FilmProgressBody, FilmProgressResponse
from storages.kafka_storage import KafkaStorage
from utils.injectors import cold_storage_injector
from utils.unpack import unpack_models

film_progress_bp = Blueprint('film-progress', __name__, url_prefix='/api/v1/film-progress')
TAG = 'Films'


@film_progress_bp.route('/', methods=['POST'])
@spec.validate(
    body=FilmProgressBody,
    resp=Response(HTTP_201=FilmProgressResponse),
    tags=[TAG],
)
@unpack_models
@jwt_required()
@cold_storage_injector
def film_progress(body: FilmProgressBody, storage: KafkaStorage) -> FilmProgressResponse:
    """ Film progress.
        ---
    """
    storage.send(body=body, topic=kafka_settings.views_topic)
    response = jsonify(message=message('send_kafka', body.user_id))
    response.status_code = HTTPStatus.CREATED
    return response
