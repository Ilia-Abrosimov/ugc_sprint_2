import json

from src.ch_handler import ClickHouseHandler


def test_get_top(ch_handler: ClickHouseHandler, load_data):
    with open('utils/response.json', 'r') as r:
        resp = json.load(r)
        print(resp)
    assert ch_handler.get_top_by_views(20) == resp
