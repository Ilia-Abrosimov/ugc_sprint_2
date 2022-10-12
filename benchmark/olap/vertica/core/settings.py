"""
Настройки для доступа к хранилищам.

"""

from pydantic import BaseSettings


class VerticaConn(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str
    autocommit: bool

    class Config:
        env_prefix = 'VERTICA_'


vertica_conn = VerticaConn()
