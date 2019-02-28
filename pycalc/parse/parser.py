"""Module with operations for expression parsing."""
from pycalc.data.tokens import TokenType, create_token, create_mult_token, FunctionToken
from pycalc.parse import parser_utils as parser_utils


class Parser:
    """Parses and validates expression.

    Attributes:
        expression: string expression that should be divided by tokens.
        const_dict: dictionary with all supported constants
        func_dict: dictionary with all supported functions
    """
    def __init__(self, expression, const_dict, func_dict):
        self.__expression = expression
        self.__const_dict = const_dict
        self.__func_dict = func_dict

    def parse_tokens(self):
        """Parse expression to tokens and validate them.

        Returns:
            list of tokens
        """
        tokens = self.__split_tokens()
        valid_tokens = self.__validate_and_add_explicit_mult(tokens)
        return valid_tokens

    def __split_tokens(self):
        """Split expression to list of tokens.

        Returns:
            list of tokens

        Raises:
            ValueError: id expression contains symbols that can not be recognized as tokens.
        """
        tokens = []
        current_token = ""
        for char in self.__expression:
            if char == " ":
                self.__add_token(current_token, tokens)
                current_token = ""
            elif char == "(" or char == "," or char == ")":
                self.__add_token(current_token, tokens)
                current_token = char
            elif char == ".":
                if len(current_token) == 0:
                    current_token = char
                elif parser_utils.is_number(current_token + char):
                    current_token = current_token + char
                else:
                    self.__add_token(current_token, tokens)
                    self.__add_token(char, tokens)
                    current_token = ""
            elif char.isdigit():
                possible_token = current_token + char
                if parser_utils.is_number(possible_token) or parser_utils.is_text(possible_token):
                    current_token += char
                else:
                    self.__add_token(current_token, tokens)
                    current_token = char
            elif parser_utils.is_operation(char):
                if parser_utils.is_operation(current_token):
                    current_token += char
                else:
                    self.__add_token(current_token, tokens)
                    current_token = char
            elif char.isalpha() or char == "_":
                if parser_utils.is_text(current_token) and not parser_utils.is_number(current_token):
                    current_token += char
                else:
                    self.__add_token(current_token, tokens)
                    current_token = char
            else:
                raise ValueError("Unexpected character: " + char)
        self.__add_token(current_token, tokens)
        return tokens

    def __add_token(self, current_token, tokens):
        """Creates token from string and adds it to common list.

        Args:
            current_token: string representation of current token
            tokens: list of all tokens
        """
        if len(current_token) > 0:
            tokens.append(create_token(current_token, self.__const_dict, self.__func_dict))

    @staticmethod
    def __validate_and_add_explicit_mult(tokens):
        """Validates list of tokens and adds explicit multiplication if it was skipped.

        Args:
            tokens: original list of tokens

        Return:
            valid list of tokens

        Raises:
            ValueError: if tokens has wrong order
        """
        bracers = 0
        result_tokens = []
        function_stack = []
        for index, token in enumerate(tokens):
            is_first_token = index == 0
            is_last_token = index == len(tokens) - 1
            prev_token = None if is_first_token else tokens[index - 1]
            if token.is_number() or token.is_function():
                if prev_token and prev_token.type in [TokenType.CONSTANT, TokenType.DIGIT, TokenType.CLOSE_BRACE]:
                    result_tokens.append(create_mult_token())
                elif prev_token and prev_token.type in [TokenType.FUNCTION]:
                    raise ValueError("Wrong tokens order")
            elif token.is_operation():
                if (is_first_token or is_last_token or
                        prev_token.type in [TokenType.OPERATION, TokenType.FUNCTION, TokenType.OPEN_BRACE,
                                            TokenType.DELIMITER]):
                    raise ValueError("Wrong tokens order")
            elif token.type == TokenType.OPEN_BRACE:
                bracers += 1
                if prev_token and prev_token.type in [TokenType.CONSTANT, TokenType.DIGIT, TokenType.CLOSE_BRACE]:
                    result_tokens.append(create_mult_token())
                if prev_token and prev_token.is_function():
                    function_stack.append((bracers, len(result_tokens) - 1, 0))
            elif token.type == TokenType.CLOSE_BRACE:
                bracers -= 1
                if bracers < 0:
                    raise ValueError("Bracers are not balanced")
                if prev_token and prev_token.type in [TokenType.DELIMITER, TokenType.OPERATION, TokenType.FUNCTION]:
                    raise ValueError("Wrong tokens order")
                if len(function_stack) > 0 and bracers + 1 == function_stack[-1][0]:
                    _, f_index, f_delimiters = function_stack.pop()
                    function = result_tokens[f_index]
                    param_count = 0 if prev_token.type == TokenType.OPEN_BRACE else f_delimiters + 1
                    result_tokens[f_index] = FunctionToken(function.function, param_count)
                elif prev_token and prev_token.type in [TokenType.OPEN_BRACE]:
                    raise ValueError("Wrong tokens order")
            elif token.type == TokenType.DELIMITER:
                if prev_token and prev_token.type in [TokenType.OPEN_BRACE, TokenType.DELIMITER, TokenType.OPERATION,
                                                      TokenType.FUNCTION]:
                    raise ValueError("Wrong tokens order")
                if len(function_stack) > 0 and bracers == function_stack[-1][0]:
                    function_stack[-1] = (function_stack[-1][0], function_stack[-1][1], function_stack[-1][2] + 1)
                else:
                    raise ValueError("Wrong tokens order")
            result_tokens.append(token)
        if bracers != 0:
            raise ValueError("Bracers are not balanced")
        return result_tokens
