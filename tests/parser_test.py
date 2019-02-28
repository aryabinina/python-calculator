import unittest

from data.tokens import *
from parse.parser import *


def get_42():
    return 42


class ParseTest(unittest.TestCase):
    def test_parse_expression_with_all_operations(self):
        tokens = Parser("1+2-10*3/4//56<9<=10==0>=4 > 9 % 3^7!=5", {}, {}).parse_tokens()
        expected_tokens = [NumberToken(1), OperationToken("+", 1), NumberToken(2), OperationToken("-", 1),
                           NumberToken(10), OperationToken("*", 2), NumberToken(3), OperationToken("/", 2),
                           NumberToken(4), OperationToken("//", 2), NumberToken(56), OperationToken("<", 0),
                           NumberToken(9), OperationToken("<=", 0), NumberToken(10), OperationToken("==", 0),
                           NumberToken(0), OperationToken(">=", 0), NumberToken(4), OperationToken(">", 0),
                           NumberToken(9), OperationToken("%", 2), NumberToken(3), OperationToken("^", 3),
                           NumberToken(7), OperationToken("!=", 0), NumberToken(5)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_expression_with_bracers(self):
        tokens = Parser("(2+(5-6))", {}, {}).parse_tokens()
        expected_tokens = [Token(TokenType.OPEN_BRACE), NumberToken(2), OperationToken("+", 1),
                           Token(TokenType.OPEN_BRACE), NumberToken(5), OperationToken("-", 1), NumberToken(6),
                           Token(TokenType.CLOSE_BRACE), Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_expression_with_float(self):
        tokens = Parser("3.4 + .09", {}, {}).parse_tokens()
        expected_tokens = [NumberToken(3.4), OperationToken("+", 1), NumberToken(0.09)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_expression_with_constants(self):
        tokens = Parser("2*pi*ten", {"pi": 3.14, "ten": 10}, {}).parse_tokens()
        expected_tokens = [NumberToken(2), OperationToken("*", 2), NumberToken(3.14), OperationToken("*", 2),
                           NumberToken(10)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_expression_with_function(self):
        tokens = Parser("test_functionReturn42(2,4,78)", {},
                        {"test_functionReturn42": get_42}).parse_tokens()
        expected_tokens = [FunctionToken(get_42, 3), Token(TokenType.OPEN_BRACE), NumberToken(2),
                           Token(TokenType.DELIMITER), NumberToken(4),
                           Token(TokenType.DELIMITER), NumberToken(78),
                           Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_unknown_symbol(self):
        parser = Parser("2 + 1#", {}, {})
        with self.assertRaisesRegex(ValueError, "Unexpected character: #"):
            parser.parse_tokens()

    def test_parse_unknown_operation(self):
        parser = Parser("2!", {}, {})
        with self.assertRaisesRegex(ValueError, "Unsupported operation: !"):
            parser.parse_tokens()

    def test_parse_unknown_constant(self):
        parser = Parser("my_const + 6", {}, {})
        with self.assertRaisesRegex(ValueError, "Unknown token: my_const"):
            parser.parse_tokens()

    def test_parse_unknown_function(self):
        parser = Parser("my_func() + 6", {}, {})
        with self.assertRaisesRegex(ValueError, "Unknown token: my_func"):
            parser.parse_tokens()

    def test_parse_wrong_bracers_count_no_close(self):
        parser = Parser("2 + ((4 - 1)*(2-2)", {}, {})
        with self.assertRaisesRegex(ValueError, "Bracers are not balanced"):
            parser.parse_tokens()

    def test_parse_wrong_bracers_count_no_open(self):
        parser = Parser("2 + ((4 - 1)*2)-2)", {}, {})
        with self.assertRaisesRegex(ValueError, "Bracers are not balanced"):
            parser.parse_tokens()

    def test_parse_wrong_bracers_order(self):
        parser = Parser(")2 + 3(", {}, {})
        with self.assertRaisesRegex(ValueError, "Bracers are not balanced"):
            parser.parse_tokens()

    def test_parse_wrong_order_empty_bracers(self):
        parser = Parser("2 + ()", {}, {})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_close_brace_after_function(self):
        parser = Parser("(2 + func_name)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_close_brace_after_delimiter(self):
        parser = Parser("(2 + func_name(1,)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_close_brace_after_operation(self):
        parser = Parser("(2 + 1*)", {}, {})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_operation_after_open_brace(self):
        parser = Parser("(*2 + 1)", {}, {})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_operation_after_operation(self):
        parser = Parser("2+-1", {}, {})
        with self.assertRaisesRegex(ValueError, "Unsupported operation: \+-"):
            parser.parse_tokens()

    def test_parse_wrong_order_operation_after_delimiter(self):
        parser = Parser("func_name(1,*3)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Unsupported operation: ,*"):
            parser.parse_tokens()

    def test_parse_wrong_order_operation_after_function(self):
        parser = Parser("func_name - 2", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_delimiter_after_open_brace(self):
        parser = Parser("func_name(,1)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_delimiter_after_operation(self):
        parser = Parser("func_name(1,>1)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Unsupported operation: ,>"):
            parser.parse_tokens()

    def test_parse_wrong_order_delimiter_after_delimiter(self):
        parser = Parser("func_name(1,,1)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_delimiter_after_function(self):
        parser = Parser("func_name,1", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_funation_after_function(self):
        parser = Parser("func_name func_name(1)", {}, {"func_name": get_42})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_delimiter_outside_function(self):
        parser = Parser("1, 3", {}, {})
        with self.assertRaisesRegex(ValueError, "Wrong tokens order"):
            parser.parse_tokens()

    def test_parse_wrong_order_extra_dot(self):
        parser = Parser("1.3.6", {}, {})
        with self.assertRaisesRegex(ValueError, "Unsupported operation: ."):
            parser.parse_tokens()

    def test_parse_add_mult_number_number(self):
        tokens = Parser("3 4", {}, {}).parse_tokens()
        expected_tokens = [NumberToken(3), OperationToken("*", 2), NumberToken(4)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_number_constant(self):
        tokens = Parser("2pi", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [NumberToken(2), OperationToken("*", 2), NumberToken(3.14)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_number_open_brace(self):
        tokens = Parser("2(3)", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [NumberToken(2), OperationToken("*", 2), Token(TokenType.OPEN_BRACE), NumberToken(3),
                           Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_number_function(self):
        tokens = Parser("2 test()", {}, {"test": get_42}).parse_tokens()
        expected_tokens = [NumberToken(2), OperationToken("*", 2), FunctionToken(get_42, 0),
                           Token(TokenType.OPEN_BRACE), Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_constant_number(self):
        tokens = Parser("pi 4", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [NumberToken(3.14), OperationToken("*", 2), NumberToken(4)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_constant_constant(self):
        tokens = Parser("pi pi", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [NumberToken(3.14), OperationToken("*", 2), NumberToken(3.14)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_constant_open_brace(self):
        tokens = Parser("pi(3)", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [NumberToken(3.14), OperationToken("*", 2), Token(TokenType.OPEN_BRACE), NumberToken(3),
                           Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_constant_function(self):
        tokens = Parser("pi test()", {"pi": 3.14}, {"test": get_42}).parse_tokens()
        expected_tokens = [NumberToken(3.14), OperationToken("*", 2), FunctionToken(get_42, 0),
                           Token(TokenType.OPEN_BRACE), Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_close_brace_number(self):
        tokens = Parser("(2)4", {}, {}).parse_tokens()
        expected_tokens = [Token(TokenType.OPEN_BRACE), NumberToken(2), Token(TokenType.CLOSE_BRACE),
                           OperationToken("*", 2), NumberToken(4)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_close_brace_constant(self):
        tokens = Parser("(2) pi", {"pi": 3.14}, {}).parse_tokens()
        expected_tokens = [Token(TokenType.OPEN_BRACE), NumberToken(2), Token(TokenType.CLOSE_BRACE),
                           OperationToken("*", 2), NumberToken(3.14)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_close_brace_open_brace(self):
        tokens = Parser("(2)(3)", {}, {}).parse_tokens()
        expected_tokens = [Token(TokenType.OPEN_BRACE), NumberToken(2), Token(TokenType.CLOSE_BRACE),
                           OperationToken("*", 2), Token(TokenType.OPEN_BRACE), NumberToken(3),
                           Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_add_mult_close_brace_function(self):
        tokens = Parser("(2)test()", {"pi": 3.14}, {"test": get_42}).parse_tokens()
        expected_tokens = [Token(TokenType.OPEN_BRACE), NumberToken(2), Token(TokenType.CLOSE_BRACE), OperationToken(
            "*", 2), FunctionToken(get_42, 0), Token(TokenType.OPEN_BRACE), Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)

    def test_parse_function_inside(self):
        tokens = Parser("test(1, test(test(), 1), 2)", {"pi": 3.14}, {"test": get_42}).parse_tokens()
        expected_tokens = [FunctionToken(get_42, 3), Token(TokenType.OPEN_BRACE), NumberToken(1),
                           Token(TokenType.DELIMITER), FunctionToken(get_42, 2), Token(TokenType.OPEN_BRACE),
                           FunctionToken(get_42, 0), Token(TokenType.OPEN_BRACE), Token(TokenType.CLOSE_BRACE),
                           Token(TokenType.DELIMITER), NumberToken(1),
                           Token(TokenType.CLOSE_BRACE),
                           Token(TokenType.DELIMITER), NumberToken(2),
                           Token(TokenType.CLOSE_BRACE)]
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
