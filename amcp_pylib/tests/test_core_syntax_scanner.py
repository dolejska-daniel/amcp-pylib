import unittest
from amcp_pylib.core.syntax import Scanner
from amcp_pylib.core.syntax.token import Token
from amcp_pylib.core.syntax.token_types import TokenType


class CoreSyntaxScannerTestCase(unittest.TestCase):

    def test_get_source(self):
        source = "source code"
        s = Scanner(source)
        self.assertEqual(s.get_source(), source)

    def test_get_source_part(self):
        sources = [
            ("source code", 0, 2, "sou"),
            ("source code", 2, 2, "sourc"),
            ("source code", 4, 3, "ource c"),
            ("source code", 9, 2, "code"),
            ("source code", 10, 2, "ode"),
        ]
        for source, position, offset, result in sources:
            with self.subTest():
                s = Scanner(source)
                s.source_position = position
                self.assertEqual(s.get_source_part(offset), result)

    def test_get_next_token_types(self):
        sources = [
            ("identifier", TokenType.IDENTIFIER),
            ("ints", TokenType.IDENTIFIER),
            ("strings", TokenType.IDENTIFIER),
            ("floats", TokenType.IDENTIFIER),
            ("int", TokenType.TYPE),
            ("string", TokenType.TYPE),
            ("float", TokenType.TYPE),
            ("-", TokenType.CONSTANT),
            ("1", TokenType.CONSTANT),
            ("10", TokenType.CONSTANT),
            (" ", TokenType.CONSTANT_SPACE),
            ("KEYWORD", TokenType.KEYWORD),
            ("KEY_WORD", TokenType.KEYWORD),
            ("[", TokenType.REQUIRED_OPEN),
            ("]", TokenType.REQUIRED_CLOSE),
            ("{", TokenType.OPTIONAL_OPEN),
            ("}", TokenType.OPTIONAL_CLOSE),
            ("|", TokenType.OPERATOR_OR),
            (":", TokenType.OPERATOR_TYPE),
            (",", TokenType.OPERATOR_COMMA),
            ("$", TokenType.UNDEFINED),
        ]
        for source, token_type in sources:
            with self.subTest():
                s = Scanner(source)
                t = s.get_next_token()
                self.assertEqual(t.get_type(), token_type)
                self.assertEqual(t.get_content(), source)

    def test_get_next_token_multiple(self):
        source = (
            "KEYWORD [identifier:TYPEA,TYPEB|KEY_WORD 10]{-[identifier:string]}",
            [
                TokenType.KEYWORD, TokenType.CONSTANT_SPACE, TokenType.REQUIRED_OPEN, TokenType.IDENTIFIER,
                TokenType.OPERATOR_TYPE, TokenType.KEYWORD, TokenType.OPERATOR_COMMA, TokenType.KEYWORD,
                TokenType.OPERATOR_OR, TokenType.KEYWORD, TokenType.CONSTANT_SPACE, TokenType.CONSTANT,
                TokenType.REQUIRED_CLOSE, TokenType.OPTIONAL_OPEN, TokenType.CONSTANT, TokenType.REQUIRED_OPEN,
                TokenType.IDENTIFIER, TokenType.OPERATOR_TYPE, TokenType.TYPE, TokenType.REQUIRED_CLOSE,
                TokenType.OPTIONAL_CLOSE
            ]
        )

        s = Scanner(source[0])
        for token_type in source[1]:
            t = s.get_next_token()
            self.assertEqual(
                t.get_type(), token_type,
                msg="Received token has unexpected type! Expected: '{expected_type}()', Received: '{received_type}'. "
                    "Source position:\n{source_position}\n{source_position_pointer}".format(
                    expected_type=TokenType.to_str(token_type), received_type=str(t),
                    source_position=s.get_source_part(8), source_position_pointer="^".rjust(9)
                )
            )

    def test_return_token_single(self):
        s = Scanner("")

        t1 = Token(TokenType.CONSTANT, "TEST")
        s.return_token(t1)

        t2 = s.get_next_token()

        self.assertEqual(t1, t2)

    def test_return_token_multiple(self):
        s = Scanner("")

        tokens = [
            Token(TokenType.CONSTANT, "TEST1"),
            Token(TokenType.CONSTANT, "TEST2"),
            Token(TokenType.CONSTANT, "TEST3"),
            Token(TokenType.CONSTANT, "TEST4"),
        ]
        for token in tokens:
            s.return_token(token)

        tokens.reverse()
        for t1 in tokens:
            t2 = s.get_next_token()
            self.assertEqual(t1, t2)


if __name__ == '__main__':
    unittest.main()
