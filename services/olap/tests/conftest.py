import json
import time
from typing import Generator

import pytest
from clickhouse_driver import Client
from core.settings import ClickHouseSettings
from src.ch_handler import ClickHouseHandler


@pytest.fixture
def ch_settings():
    return ClickHouseSettings(host='localhost', port=None, alt_hosts=None)


@pytest.fixture
def client(ch_settings: ClickHouseSettings) -> Client:
    print(f'{ch_settings = }')
    client = Client(host=ch_settings.host, port=ch_settings.port, alt_hosts=ch_settings.alt_hosts)
    yield client


@pytest.fixture
def ch_handler(client: Client) -> Generator:
    handler = ClickHouseHandler(client)
    yield handler


@pytest.fixture
def load_data(client: Client, data_file: str = 'utils/src.json') -> None:
    with open(data_file) as f:
        data = json.load(f)
    print(f'{data = }')
    query = 'INSERT INTO default.views (id, user_id, film_id, viewed_frame) VALUES'
    client.execute(query, data)
    time.sleep(2)
