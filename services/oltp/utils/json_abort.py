"""
В случае ошибочного запроса к хранилищу выполняется вызов данной функции.

"""

from flask import abort, jsonify, make_response


def json_abort(status: int, message: str):
    abort(make_response(jsonify(message=message), status))
