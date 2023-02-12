from enum import StrEnum

class Operator(StrEnum):
    # Arithmetic Operators
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULT = "*"
    MOD = "%"
    EXPONENT = "**"

    # Chaining Operators
    DOT = "."
    OPTION_DOT = "?."

    # Comparison Operators
    EQ = "=="
    NOT_EQ = "!="
    GT = ">"
    LT = "<"
    GT_EQ = ">="
    LT_EQ = "<="

    # Boolean Operators
    AND = "and"
    OR = "or"
    NOT = "not"

    # Bitwise Operators
    BIN_LEFT = "<<"
    BIN_RIGHT = ">>"
    BIN_ZERO_RIGHT = ">>>"
    BIN_OR = "|"
    BIN_XOR = "^"
    BIN_AND = "&"
    BIN_NOT = "~"

    # Miscellaneous Operators
    RANGE = ".."
    COALESCE = "??"
    IN = "in"

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls)
        if value in ["+", "-"]:
            obj._is_binary_ = None
        elif value in ["!", "not", "~"]:
            obj._is_binary_ = False
        else:
            obj._is_binary_ = True
        return obj

    @property 
    def is_unary(self):
        return self._is_binary_


class AssignmentOperator(StrEnum):
    pass



