from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """ Базовый класс извлечения данных из хранилища событий """

    @abstractmethod
    def consume(self):
        """ """

    @abstractmethod
    def stop_consuming(self):
        """ """

    @abstractmethod
    def commit(self):
        """ """
