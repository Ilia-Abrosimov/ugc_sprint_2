from http import HTTPStatus

from core.config import settings
from flask_jwt_extended import create_access_token
from messages.messages import message


def test_film_progress(app, client):
    valid_data = {
        "film_id": "b11188af-2451-47e7-948d-ae1fabfb0d74",
        "user_id": "cf57432e-809e-4353-adbd-9d5c0d733868",
        "progress": 123
    }
    url = settings.test_api_url + 'film-progress/'
    access_token = create_access_token(identity=123)
    access_headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post(url, json=valid_data, headers=access_headers)
    data = response.json
    assert response.status_code == HTTPStatus.CREATED
    assert data.get("message") == message('send_kafka', valid_data['user_id'])
