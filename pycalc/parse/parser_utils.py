"""Module with utilities functions and constants for expression parsing."""
import re

# Dictionary with all supported operations and their priorities.
SUPPORTED_OPERATIONS = {
    "+": 1, "-": 1,
    "*": 2, "/": 2, "//": 2, "%": 2,
    "^": 3,
    "<": 4, "<=": 4, "==": 4, "!=": 4, ">=": 4, ">": 4
}
# Regular expression to match operations.
__OPERATION_REGEXP = r'^[\\+-/%^*<>=!]+$'
# Regular expression to match constants and functions names.
__TEXT_REGEXP = r'^[A-Za-z0-9_]+$'


def is_number(number):
    """ Determines whether argument is a number or not. """
    return number.replace(".", "", 1).isdigit()


def is_operation(text):
    """ Determines whether argument is a operation or not. """
    return re.match(__OPERATION_REGEXP, text)


def is_text(text):
    """ Determines whether argument is a text or not. """
    return re.match(__TEXT_REGEXP, text)