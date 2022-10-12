"""
Запуск теста ClickHouse (вариант с шардированием).

"""

from threading import Thread

from click_house.client import CHClient
from src.settings import settings
from utils.logger import ch_logger
from utils.timer import Timer

pending = True


def write_data(table: str = 'views'):
    client = CHClient()
    for _ in range(int(settings.data_volume / settings.ch_batch_size)):
        client.add_data('default', table, settings.ch_batch_size)


def read_data(table: str = 'views'):
    client = CHClient()
    for _ in range(settings.requests_num):
        client.read_data('default', table)


def read_in_parallel(table: str = 'views'):
    global pending
    client = CHClient()
    while pending:
        client.read_data('default', table)


def write_read(table: str = 'views'):
    global pending
    write = Thread(target=write_data, args=(table,))
    read = Thread(target=read_in_parallel, args=(table,))
    write.start()
    read.start()
    write.join()
    pending = False
    read.join()


if __name__ == '__main__':
    with Timer(logger=ch_logger, message=f'write data DV={settings.data_volume} BS={settings.ch_batch_size}'):
        write_data()

    with Timer(logger=ch_logger, message=f'read data DV={settings.data_volume} RN={settings.requests_num}'):
        read_data()

    with Timer(
        logger=ch_logger,
        message=f'write/read data DV={settings.data_volume} BS={settings.ch_batch_size} RN={settings.requests_num}',
    ):
        write_read()
