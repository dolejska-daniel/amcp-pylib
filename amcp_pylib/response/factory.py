from .parser import Parser

from .base import Base
from .info_response import InfoResponse
from .success_response import SuccessResponse
from .client_error_response import ClientErrorResponse
from .server_error_response import ServerErrorResponse


class Factory:

    @staticmethod
    def create_from_bytes(data: bytes) -> Base:
        """ Creates corresponding response class instance based on input data. """
        data = data.decode("UTF-8")

        # Parse status code from response bytes
        status_code, *_ = Parser.parse_response_status_header(data)

        # Select appropriate class
        if status_code < 200:
            return InfoResponse(data)
        elif status_code < 400:
            return SuccessResponse(data)
        elif status_code < 500:
            return ClientErrorResponse(data)
        else:
            return ServerErrorResponse(data)
