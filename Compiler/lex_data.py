from enum import StrEnum
import re


# An Enum class for defining the available operators in the language.
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
    BIN_OR = "||"
    BIN_XOR = "^"
    BIN_AND = "&&"
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


# An Enum class for defining the available assignment operators in the language. 
# I've chosen to make this a separate class because assignment operators are 
# allowed only in special places.
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


class Delimiter(StrEnum):
    O_PAREN = "("
    C_PAREN = ")"
    O_BRACE = "{"
    C_BRACE = "}"
    O_BRACKET = "["
    C_BRACKET = "]"
    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = "'"
    LAMBDA_DELIM = "|"
    REGEX_QUOTE = "`"


class Formats:
    IDENTIFIER_REGEX = re.compile(r"(?!^_$)^[a-zA-Z_]+\w*$")
    is_identifier = lambda string: Formats.IDENTIFIER_REGEX.search(string) is not None

    NUMBER_REGEX = re.compile(r"^(?!^0[^.eE])((\d+(\.\d*)?)|(\.\d+))([eE][+-]?\d+)?$")
    is_number = lambda string: Formats.NUMBER_REGEX.search(string) is not None

    BIGINT_REGEX = re.compile(r"^(0|([1-9]+\d*))n$")
    is_bigint = lambda string: Formats.BIGINT_REGEX.search(string) is not None

    OCTAL_REGEX = re.compile(r"^0o[0-7]+n?$")
    is_octal = lambda string: Formats.OCTAL_REGEX.search(string) is not None

    HEX_REGEX = re.compile(r"^0x[0-9a-fA-F]+n?")
    is_hex = lambda string: Formats.HEX_REGEX.search(string) is not None

    BINARY_REGEX = re.compile(r"^0b[01]+n?")
    is_binary = lambda string: Formats.BINARY_REGEX.search(string) is not None
