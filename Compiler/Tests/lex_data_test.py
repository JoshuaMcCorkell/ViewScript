import sys
sys.path.append("..")
from lex_data import Formats


def test_identifier_regex():
    identifier_tests = [
        ("", False),
        ("_", False),
        ("x", True),
        ("abcdefgHIJKLMNOPqrStUvwXYz", True),
        ("ABCDEFGhijklmnopQRsTuVWxyZ", True),
        ("a1234567890", True),
        ("1ABC456", False),
        ("_1", True),
        ("_variable65", True),
        ("abcd123!", False),
        ("ABCD%", False),
        ('n"', False),
    ]
    for test, result in identifier_tests:
        assert Formats.is_identifier(test) == result


def test_number_regex():
    number_tests = [
        ("0", True),
        ("1", True),
        ("01", False),
        ("0.", True),
        ("1.", True),
        (".1", True),
        (".0", True),
        (".0e0", True),
        (".20e-458", True),
        ("a", False),
        ("$", False),
        ("1234567890", True),
        ("123.0", True),
        ("01234.0", False),
        ("0o12", False),
        ("0x12", False),
        ("0b10", False),
        ("12345n", False),
        ("5403900.00293700", True),
        ("0e0", True),
        ("1e1", True),
        ("45.e2", True),
        ("0.0e0", True),
        ("58.e15.", False),
        ("29.25E-19", True),
        ("15n", False),
    ]
    for test, result in number_tests:
        assert Formats.is_number(test) == result