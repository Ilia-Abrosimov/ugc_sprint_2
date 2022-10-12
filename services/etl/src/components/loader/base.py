from abc import ABC, abstractmethod


class BaseLoader(ABC):
    """ Базовый класс загрузки данных в OLAP-хранилище """

    @abstractmethod
    def upload_data(self, **kwargs) -> None:
        """ Вставка данных, поступающих из OLTP хранилища """

    @abstractmethod
    def _add_data(self, **kwargs) -> None:
        """ Вставка данных, поступающих из OLTP хранилища """
