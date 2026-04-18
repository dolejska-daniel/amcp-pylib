import unittest

from amcp_pylib.core import Command
from amcp_pylib.module.basic import ADD, CALL, CLEAR_ALL, LOADBG, PLAY
from amcp_pylib.module.data import DATA_STORE
from amcp_pylib.module.query import BEGIN, OSC_SUBSCRIBE


class CommandSerializationTestCase(unittest.TestCase):
    def test_commands_terminate_with_crlf_and_encode_utf8(self):
        command = PLAY(video_channel=1, clip="åäö")

        self.assertEqual(str(command), "PLAY 1-0 åäö\r\n")
        self.assertEqual(bytes(command), "PLAY 1-0 åäö\r\n".encode("UTF-8"))

    def test_quotes_and_escapes_string_arguments_only_when_needed(self):
        command = DATA_STORE(name="folder/my data", data='quote " slash \\ newline\nend')

        self.assertEqual(
            str(command),
            'DATA STORE "folder/my data" "quote \\" slash \\\\ newline\\nend"\r\n',
        )

    def test_raw_arguments_allow_modern_producer_and_consumer_parameters(self):
        command = ADD(
            video_channel=1,
            consumer="STREAM",
            parameters=["udp://localhost:5004", "-vcodec", "libx264", "-filter:v", "scale=240:180"],
        )

        self.assertEqual(
            str(command),
            "ADD 1 STREAM udp://localhost:5004 -vcodec libx264 -filter:v scale=240:180\r\n",
        )

    def test_raw_string_arguments_preserve_existing_call_param_usage(self):
        self.assertEqual(str(CALL(video_channel=1, layer=2, param="SEEK 25")), "CALL 1-2 SEEK 25\r\n")

    def test_modern_basic_commands_are_available(self):
        self.assertEqual(str(CLEAR_ALL()), "CLEAR ALL\r\n")
        self.assertEqual(str(LOADBG(channel=1, clip="MISSING", clear_on_404="clear_on_404")), "LOADBG 1 MISSING CLEAR_ON_404\r\n")

    def test_request_id_prefix_for_batching(self):
        self.assertEqual(str(BEGIN(request_id="abc")), "REQ abc BEGIN\r\n")
        self.assertEqual(str(Command.raw("COMMIT", request_id="batch-1")), "REQ batch-1 COMMIT\r\n")

    def test_osc_subscription_command(self):
        self.assertEqual(str(OSC_SUBSCRIBE(port=6250)), "OSC SUBSCRIBE 6250\r\n")


if __name__ == "__main__":
    unittest.main()
