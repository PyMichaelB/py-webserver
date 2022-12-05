from enum import Enum

class Method(Enum):
    GET = 'GET'
    POST = 'POST'

class Status(Enum):
    OK = 200
    INTERNAL_SERVER_ERROR = 500
    NOT_FOUND = 404
    BAD_REQUEST = 400