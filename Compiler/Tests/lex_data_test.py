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
        ("129-", False),
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
        ("45.23e+123", True),
        ("15n", False),
    ]
    for test, result in number_tests:
        assert Formats.is_number(test) == result


def test_bigint_regex():
    bigint_tests = [
        ("0", False),
        ("1234", False),
        ("0n", True),
        ("n", False),
        ("9n", True),
        ("2345678n", True),
        ("0583n", False),
        ("123.n", False),
        ("12e2n", False),
        (".2n", False),
    ]
    for test, result in bigint_tests:
        assert Formats.is_bigint(test) == result


def test_hex_regex():
    hex_tests = [
        ("0", False),
        ("1234", False),
        ("123n", False),
        ("0x0", True),
        ("0x", False),
        ("0XA", True),
        ("0x12ab853CD4", True),
        ("0X00F", True),
        ("0x1FDe2n", True),
        ("0xA12&", False),
        ("00x1", False),
        ("0x24.3", False),
        ("0X5.", False),
        ("0o12", False),
        ("0b101", False),
    ]
    for test, result in hex_tests:
        assert Formats.is_hex(test) == result


def test_octal_regex():
    octal_tests = [
        ("0", False),
        ("1234", False),
        ("123n", False),
        ("0O0", True),
        ("0o", False),
        ("0o7", True),
        ("0o1234567", True),
        ("0O12340n", True),
        ("0O0024", True),
        ("0o15#", False),
        ("0o1278", False),
        ("00o1", False),
        ("0O13e32", False),
        ("0o24.3", False),
        ("0o5.", False),
        ("0x12", False),
        ("0b101", False),
    ]
    for test, result in octal_tests:
        assert Formats.is_octal(test) == result


def test_binary_regex():
    binary_tests = [
        ("0", False),
        ("1010", False),
        ("100n", False),
        ("0B0", True),
        ("0b", False),
        ("0b1", True),
        ("0B1110100100", True),
        ("0B001110", True),
        ("0b00101001n", True),
        ("0b1011~", False),
        ("0b101010012", False),
        ("00b11", False),
        ("0b11e10", False),
        ("0b110.1", False),
        ("0b1.", False),
        ("0x101", False),
        ("0o103", False),
    ]
    for test, result in binary_tests:
        assert Formats.is_binary(test) == result