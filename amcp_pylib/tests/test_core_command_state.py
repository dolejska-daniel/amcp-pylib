import unittest

from amcp_pylib.module.query import VERSION


class CoreCommandStateTestCase(unittest.TestCase):
    def test_command_calls_do_not_reuse_previous_arguments(self):
        self.assertEqual(str(VERSION(component="server")).strip(), 'VERSION "server"')
        self.assertEqual(str(VERSION()).strip(), "VERSION")


if __name__ == "__main__":
    unittest.main()
