"""
Запуск теста Vertica (вариант с одной таблицей).

"""

from threading import Thread

from src.settings import settings
from utils.logger import vertica_logger
from utils.timer import Timer
from vertica.client import VerticaClient


def write_data():
    client = VerticaClient()
    for _ in range(int(settings.data_volume / settings.vertica_batch_size)):
        client.add_data(settings.vertica_batch_size)
    client.close_conn()


def read_data():
    client = VerticaClient()
    for _ in range(settings.requests_num):
        client.read_data()
    client.close_conn()


def read_in_parallel():
    global pending
    client = VerticaClient()
    while pending:
        client.read_data()
    client.close_conn()


def write_read():
    global pending
    write = Thread(target=write_data)
    read = Thread(target=read_in_parallel)
    write.start()
    read.start()
    write.join()
    pending = False
    read.join()


if __name__ == '__main__':
    client = VerticaClient()
    client.create_table()

    with Timer(
        logger=vertica_logger,
        message=f'write data DV={settings.data_volume} BS={settings.vertica_batch_size}',
    ):
        write_data()

    with Timer(
        logger=vertica_logger,
        message=f'read data DV={settings.data_volume} RN={settings.requests_num}',
    ):
        read_data()

    pending = True
    with Timer(
        logger=vertica_logger,
        message=f'write/read data DV={settings.data_volume} BS={settings.vertica_batch_size} '
                f'RN={settings.requests_num}',
    ):
        write_read()

    client.close_conn()
