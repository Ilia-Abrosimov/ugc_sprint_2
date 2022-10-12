from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    """ Базовый класс преобразования данных """

    @abstractmethod
    def transform(self, records: dict) -> dict:
        """ """
