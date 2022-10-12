"""
Запуск теста ClickHouse (вариант с одной таблицей).

"""

from click_house.client import CHClient
from src.settings import settings
from tests.click_house_shard.test import read_data, write_data, write_read
from utils.logger import ch_logger_reg
from utils.timer import Timer

TABLE_NAME = 'views_regular'


if __name__ == '__main__':
    client = CHClient()
    client.create_table(TABLE_NAME)

    with Timer(logger=ch_logger_reg, message=f'write data DV={settings.data_volume} BS={settings.ch_batch_size}'):
        write_data(TABLE_NAME)

    with Timer(logger=ch_logger_reg, message=f'read data DV={settings.data_volume} RN={settings.requests_num}'):
        read_data(TABLE_NAME)

    with Timer(
            logger=ch_logger_reg,
            message=f'write/read data DV={settings.data_volume} BS={settings.ch_batch_size} RN={settings.requests_num}',
    ):
        write_read(TABLE_NAME)
