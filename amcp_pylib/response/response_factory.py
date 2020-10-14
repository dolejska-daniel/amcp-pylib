from amcp_pylib.response.types import *

from .response_base import ResponseBase


class ResponseFactory:

    @staticmethod
    def create_from_bytes(data: bytes) -> ResponseBase:
        """ Creates corresponding response class instance based on input data. """
        data = data.decode("UTF-8")

        # parse status code from response bytes
        status_code, *_ = ResponseBase.parse_response_status_header(data)

        # select appropriate class
        if status_code < 200:
            return InfoResponse(data)

        elif status_code < 400:
            return SuccessResponse(data)

        elif status_code < 500:
            return ClientErrorResponse(data)

        else:
            return ServerErrorResponse(data)
