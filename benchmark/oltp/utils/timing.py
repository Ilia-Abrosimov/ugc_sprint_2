import os
import time

from core import settings
from loguru import logger

log_file = settings.LOG_FILE
logger.add(log_file, rotation='100 MB')


class Timing:
    def __init__(self, message: str = '', n_messages=settings.MSG_COUNT, msg_size=settings.MSG_SIZE):
        self.start_time = None
        self.message = message
        self.n_messages = n_messages
        self.msg_size = msg_size

    def start(self):
        self.start_time = time.time()

    def stop(self):
        timing = time.time() - self.start_time
        self.start_time = None
        self.results(timing)
        return timing

    def results(self, timing):
        logger.info(f'{os.path.abspath(log_file)}')
        logger.info(f'{self.message}')
        logger.info(f'Processed {self.n_messages} messsages in {timing:.2f} seconds')
        logger.info(f'{(self.msg_size * self.n_messages) / timing / (1024 * 1024):.2f} MB/s')
        logger.info(f'{self.n_messages / timing:.2f} Msgs/s')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
