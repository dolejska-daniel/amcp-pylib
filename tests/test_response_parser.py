import unittest

from amcp_pylib.exceptions import AMCPParseError, AMCPResponseError
from amcp_pylib.response import ResponseCodeClass, ResponseFactory
from amcp_pylib.response.types import ClientErrorResponse, InfoResponse, SuccessResponse


class ResponseParserTestCase(unittest.TestCase):
    def test_success_without_data(self):
        response = ResponseFactory.create_from_bytes(b"202 PLAY OK\r\n")

        self.assertIsInstance(response, SuccessResponse)
        self.assertEqual(response.code, 202)
        self.assertEqual(response.code_description, "PLAY")
        self.assertEqual(response.status, "OK")
        self.assertEqual(response.data, [])
        self.assertTrue(response.ok)

    def test_single_data_line(self):
        response = ResponseFactory.create_from_bytes(b"201 VERSION OK\r\n2.4.3 Stable\r\n")

        self.assertEqual(response.data, ["2.4.3 Stable"])
        self.assertEqual(response.data_str, "2.4.3 Stable")

    def test_multiline_response_with_extra_crlf(self):
        response = ResponseFactory.create_from_bytes(b"200 INFO OK\r\n1 PAL PLAYING\r\n2 1080p5000 PLAYING\r\n\r\n")

        self.assertEqual(response.code_class, ResponseCodeClass.SUCCESS)
        self.assertEqual(response.data, ["1 PAL PLAYING", "2 1080p5000 PLAYING"])

    def test_request_id_prefix_is_preserved(self):
        response = ResponseFactory.create_from_bytes(b"RES abc 202 COMMIT OK\r\n")

        self.assertEqual(response.request_id, "abc")
        self.assertEqual(response.code_description, "COMMIT")

    def test_nonstandard_error_header_is_preserved(self):
        response = ResponseFactory.create_from_bytes(b"403 OSC SUBSCRIBE BAD PORT\r\n")

        self.assertIsInstance(response, ClientErrorResponse)
        self.assertEqual(response.header_text, "OSC SUBSCRIBE BAD PORT")
        self.assertEqual(response.code_description, "OSC SUBSCRIBE BAD PORT")
        self.assertIsNone(response.status)
        with self.assertRaises(AMCPResponseError):
            response.raise_for_status()

    def test_ping_response(self):
        response = ResponseFactory.create_from_bytes(b"PONG token\r\n")

        self.assertIsInstance(response, InfoResponse)
        self.assertEqual(response.code, 0)
        self.assertEqual(response.code_description, "PONG")
        self.assertEqual(response.data, ["token"])

    def test_invalid_status_line_raises_parse_error(self):
        with self.assertRaises(AMCPParseError):
            ResponseFactory.create_from_bytes(b"not an amcp response\r\n")

    def test_response_framing_detection(self):
        self.assertFalse(ResponseFactory.is_complete(b"201 VERSION OK\r\n"))
        self.assertTrue(ResponseFactory.is_complete(b"201 VERSION OK\r\n2.4.3 Stable\r\n"))
        self.assertFalse(ResponseFactory.is_complete(b"200 INFO OK\r\n1 PAL\r\n"))
        self.assertTrue(ResponseFactory.is_complete(b"200 INFO OK\r\n1 PAL\r\n\r\n"))


if __name__ == "__main__":
    unittest.main()
