import unittest

from amcp_pylib.core.syntax import Parser, Scanner
from amcp_pylib.core.syntax.token import Token
from amcp_pylib.core.syntax.token_types import TokenType


class CoreSyntaxStateTestCase(unittest.TestCase):
    def test_scanner_instances_do_not_share_position(self):
        first = Scanner("FIRST")
        self.assertEqual(first.get_next_token().get_content(), "FIRST")

        second = Scanner("SECOND")
        self.assertEqual(second.get_next_token().get_content(), "SECOND")

    def test_scanner_instances_do_not_share_returned_tokens(self):
        first = Scanner("")
        first.return_token(Token(TokenType.CONSTANT, "FIRST"))

        second = Scanner("SECOND")
        self.assertEqual(second.get_next_token().get_content(), "SECOND")

    def test_try_get_token_without_constraint_returns_token(self):
        parser = Parser(Scanner("identifier"))

        token = parser.try_get_token(token_type=None)

        self.assertEqual(token.get_type(), TokenType.IDENTIFIER)
        self.assertEqual(token.get_content(), "identifier")


if __name__ == "__main__":
    unittest.main()
