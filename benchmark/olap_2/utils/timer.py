"""
Таймер для замеров времени.

Может использоваться как декоратор, как контекстный менеджер
или через создание экземпляра класса с вызовом необходимых методов.

Параметр 'repeat' - количество повторов выполнения операции (актуально для тестов на скорость
слабонагруженных операций, работает только при использовании таймера в качестве декоратора).

"""

import functools
import logging
import time


class Timer:

    def __init__(self, logger: logging, message: str = '', repeat: int = 1):
        self.start_time = None
        self.message = message
        self.repeat = repeat
        self.logger = logger

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                result = None
                for _ in range(self.repeat):
                    result = func(*args, **kwargs)
                return result

        return wrapper_timer

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None
        print(f'{self.message.ljust(45)}-> {elapsed_time}')
        self.logger.info(f'{self.message.ljust(45)}-> {elapsed_time}')

        return elapsed_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
