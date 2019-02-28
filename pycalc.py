"""Module for expression evaluation."""
import argparse
import numbers
import sys
from data.tokens import TokenType
from parse.parser import Parser


def load(module_name, constants_dict, functions_dict):
    """Loads module and aggregate all public constants and functions.

    Args:
        module_name: name of module to load
        constants_dict: dictionary with all loaded constants
        functions_dict: dictionary with all loaded functions
    """
    module = __import__(module_name)
    for name, value in vars(module).items():
        if not name.startswith("_"):
            if callable(value):
                functions_dict[name] = value
            elif isinstance(value, numbers.Number):
                constants_dict[name] = value


def reverse_polish_notation(tokens):
    """Converts tokens list to reverse polish notation.

    Args:
        tokens: tokens list in direct order

    Returns:
        tokens in reverse polish notation
    """
    result, stack = [], []
    for token in tokens:
        if token.is_number():
            result.append(token)
        if token.is_function():
            stack.append(token)
        if token.type == TokenType.DELIMITER:
            while len(stack) > 0 and stack[-1].type != TokenType.OPEN_BRACE:
                result.append(stack.pop())
        if token.type == TokenType.OPEN_BRACE:
            stack.append(token)
        if token.type == TokenType.CLOSE_BRACE:
            while stack[-1].type != TokenType.OPEN_BRACE:
                result.append(stack.pop())
            if len(stack) > 0 and stack[-1].type == TokenType.OPEN_BRACE:
                stack.pop()
            if len(stack) > 0 and stack[-1].type == TokenType.FUNCTION:
                result.append(stack.pop())
        if token.type == TokenType.OPERATION:
            while (len(stack) > 0 and stack[-1].type == TokenType.OPERATION and
                   stack[-1].priority >= token.priority):
                result.append(stack.pop())
            stack.append(token)
    while len(stack) > 0:
        result.append(stack.pop())
    return result


def calculate(tokens):
    """Calculates result.

    Args:
        tokens: tokens in reverse polish notation.

    Returns:
         result of expression
    """
    stack = []
    for token in tokens:
        if token.is_number():
            stack.append(token)
        else:
            args = []
            args_count = token.param_count if token.is_function() else 2
            for i in range(args_count):
                args.insert(0, stack.pop().value)
            stack.append(token.calculate(tuple(args)))
    return stack[0].value


def evaluate(modules, expression):
    """Parses and calculates expression result.

    Args:
        modules: list of module names that have to be used
        expression: expression to evaluate

    Returns:
        result of expression evaluation
    """
    modules.insert(0, "math")
    constants_dict = {}
    functions_dict = {"abs": abs, "round": round}
    for module in modules:
        load(module, constants_dict, functions_dict)
    tokens = Parser(expression, constants_dict, functions_dict).parse_tokens()
    result = calculate(reverse_polish_notation(tokens))
    return result


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
        parser.add_argument("expression", metavar="EXPRESSION", type=str, help="expression string to evaluate")
        parser.add_argument("-m", "--use-modules", metavar="MODULE", action="append", nargs='+', help="additional modules to use")
        args = parser.parse_args()
        use_modules = []
        if args.use_modules:
            use_modules = [module for sublist in args.use_modules for module in sublist]
        result = evaluate(use_modules, args.expression)
        print(result)
    except Exception as e:
        sys.exit("ERROR: " + str(e))

