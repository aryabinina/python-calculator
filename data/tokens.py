"""Module with all supported tokens, their behavior and functions for their creation."""
from enum import Enum
from parse import parser_utils


class TokenType(Enum):
    """All supported token types."""
    DIGIT = 0
    OPERATION = 1
    FUNCTION = 2
    OPEN_BRACE = 3
    CLOSE_BRACE = 4
    CONSTANT = 5
    DELIMITER = 6


class Token:
    """Base object.

    Attributes:
        type: token's type

    """
    def __init__(self, t_type):
        self.type = t_type

    def __repr__(self):
        return str(self.type)

    def __eq__(self, other):
        return self.type == other.type

    @staticmethod
    def is_operation():
        """Returns True is current token represents operation."""
        return False

    @staticmethod
    def is_number():
        """Returns True is current token represents number or constant."""
        return False

    @staticmethod
    def is_function():
        """Returns True is current token represents function."""
        return False


class NumberToken(Token):
    """Token to represent number or boolean.

    Attributes:
        value: number/boolean value
    """
    def __init__(self, value):
        super().__init__(TokenType.DIGIT)
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def is_number(self):
        return True


class FunctionToken(Token):
    """Token to represent function.

    Attributes:
        function: callable function
        param_count: count of function arguments
    """
    def __init__(self, function, param_count=0):
        super().__init__(TokenType.FUNCTION)
        self.function = function
        self.param_count = param_count

    def __repr__(self):
        return str(str(self.function) + ":" + str(self.param_count))

    def __eq__(self, other):
        return self.function == other.function and self.param_count == other.param_count

    def is_function(self):
        return True

    def calculate(self, args):
        """Evaluates function.

        Args:
            args: function argument

        Returns:
            result of function evaluation
        """
        if len(args) != self.param_count:
            raise ValueError("Unexpected arguments count for function: " + str(self))
        result = self.function(*args)
        return NumberToken(result)


class OperationToken(Token):
    """Token to represent mathematical operation.

        Attributes:
            operation: operation as string value
            priority: operation priority
        """
    def __init__(self, operation, priority=0):
        super().__init__(TokenType.OPERATION)
        self.operation = operation
        self.priority = priority

    def __repr__(self):
        return str(self.operation)

    def __eq__(self, other):
        return self.operation == other.operation

    def is_operation(self):
        return True

    def calculate(self, args):
        """Evaluates operation.

        Args:
            args: arguments for operation

        Returns:
             result of operation evaluation

        Raises:
            ValueError: for unknown operation and if arguments count is not suitable for operation
        """
        if len(args) != 2:
            raise ValueError("Operation {0} requires 2 arguments. Args: {1}".format(self.operation, args))
        arg1 = args[0]
        arg2 = args[1]
        if self.operation == "+":
            return NumberToken(arg1 + arg2)
        if self.operation == "-":
            return NumberToken(arg1 - arg2)
        if self.operation == "*":
            return NumberToken(arg1 * arg2)
        if self.operation == "/":
            return NumberToken(arg1 / arg2)
        if self.operation == "//":
            return NumberToken(arg1 // arg2)
        if self.operation == "%":
            return NumberToken(arg1 % arg2)
        if self.operation == "^":
            return NumberToken(arg1 ** arg2)
        if self.operation == "<":
            return NumberToken(arg1 < arg2)
        if self.operation == "<=":
            return NumberToken(arg1 <= arg2)
        if self.operation == "==":
            return NumberToken(arg1 == arg2)
        if self.operation == "!=":
            return NumberToken(arg1 != arg2)
        if self.operation == ">=":
            return NumberToken(arg1 >= arg2)
        if self.operation == ">":
            return NumberToken(arg1 > arg2)
        raise ValueError("UNSUPPORTED CALCULATION FOR ", self, args)


def create_mult_token():
    """Creates token for multiplication operation."""
    return OperationToken("*", parser_utils.SUPPORTED_OPERATIONS.get("*", 0))


def create_token(token_str, const_dict, func_dict):
    """Creates token from string.

    Args:
        token_str: string token representation
        const_dict: dictionary with all supported constants names and their values
        func_dict: dictionary with all supported function names and their values

    Returns:
        token

    Raises:
        ValueError: for unknown tokens
    """
    if token_str == "(":
        return Token(TokenType.OPEN_BRACE)
    if token_str == ")":
        return Token(TokenType.CLOSE_BRACE)
    if token_str == ",":
        return Token(TokenType.DELIMITER)
    if parser_utils.is_number(token_str):
        return NumberToken(float(token_str) if "." in token_str else int(token_str))
    if parser_utils.is_operation(token_str):
        if token_str in parser_utils.SUPPORTED_OPERATIONS.keys():
            return OperationToken(token_str, parser_utils.SUPPORTED_OPERATIONS.get(token_str, 0))
        else:
            raise ValueError("Unsupported operation: " + token_str)
    if token_str in const_dict:
        return NumberToken(const_dict[token_str])
    if token_str in func_dict:
        return FunctionToken(func_dict[token_str])
    raise ValueError("Unknown token: " + token_str)


