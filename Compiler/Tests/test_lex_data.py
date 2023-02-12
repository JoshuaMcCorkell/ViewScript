from lex_data import Formats


def test_identifier_regex():
    identifier_tests = [
        ("_hello", True),
        ("1jos", False),
        ("_", False),
        ("J10d0_wjod", True),
        ("Jdjo5%", False),
        ('ghdl"', False),
    ]
    for test, result in identifier_tests:
        assert Formats.is_identifier(test) == result


def test_number_regex():
    number_tests = [
        ("1", True),
        ("0", True),
        ("05", False),
        ("3450d", False),
        ("12359800", True),
        ("1e1", True),
        ("45e-14", True),
        ("34n", True),
        ("4.5n", False),
        ("6.4", True),
        ("12.0e4", True),
        ("12.5e05", True),
        ("902.050e0.5", False),
        ("420.2e5n", False),
        (".2", True),
        (".45e5", True),
    ]
    for test, result in number_tests:
        assert Formats.is_number(test) == result
