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
    def is_binary(self):
        return self._is_binary_


class AssignmentOperator(StrEnum):
    # Arithmetic Assignment Operators
    ASSIGN = "="
    PLUS = "+="
    MINUS = "-="
    MULT = "*="
    DIVIDE = "/="
    EXPONENT = "**="
    MOD = "%="

    # Bitwise Assignment Operators
    BIN_LEFT = "<<="
    BIN_RIGHT = ">>="
    BIN_ZERO_RIGHT = ">>>="
    BIN_OR = "|="
    BIN_XOR = "^="
    BIN_AND = "&="

    # Miscellaneous Assignment Operators
    COALESCE = "??="


class Keyword(StrEnum):
    # Declarations
    FUNCTION = "fn"
    LET = "let"
    CONST = "const"
    GLOBAL = "GLOBAL"

    # Statements
    DELETE = "del"
    RETURN = "return"
    BREAK = "break"
    YIELD = "yield"
    CONTINUE = "continue"

    # Control Structures
    TRY = "try"
    EXCEPT = "except"
    FINALLY = "finally"
    RAISE = "raise"

    IF = "if"
    ELIF = "elif"
    ELSE = "else"

    FOR = "for"
    WHILE = "while"
    LOOP = "loop"

    SWITCH = "switch"
    CASE = "case"

    # Special Constants
    THIS = "this"
    SUPER = "super"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    UNDEFINED = "undefined"
    INFINITY = "infinity"

    # Miscellaneous
    DEBUG = "_debug_"
    UNDERSCORE = "_"

    # Planned Features
    _ARGUMENTS = "arguments"
    _ASYNC = "async"
    _AWAIT = "await"
    _ENUM = "enum"
    _IMPORT = "import"
    _EXPORT = "export"

    # Reserved (Not in use)
    _CLASS = "class"
    _GOTO = "goto"
    _PACKAGE = "package"
    _DELETE = "delete"
    _IMPLEMENTS = "implements"
    _WITH = "with"
    _DO = "do"
    _FUNCTION = "function"
    _INTERFACE = "interface"
    _NEW = "new"
    _STATIC = "static"
    _VOID = "void"





if __name__ == "__main__":
    print(Operator.AND.is_binary)
    print(Operator.PLUS.is_binary)
    print(Operator.NOT.is_binary)
