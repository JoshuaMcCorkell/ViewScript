from enum import StrEnum, auto
import string
import re


letters = set(string.ascii_letters + "_")
digits = set(string.digits)
reg_chars = letters + digits
whitespace = set(string.whitespace)
symbols = set(set(string.printable) - reg_chars - whitespace)


class OperatorType(StrEnum):
    PREFIX = auto()
    POSTFIX = auto()
    BINARY = auto()
    ASSIGNMENT = auto()


# An Enum class for defining the available operators in the language.
class Operator(StrEnum):
    # Arithmetic Operators
    PLUS = "+", OperatorType.BINARY, OperatorType.PREFIX
    MINUS = "-", OperatorType.BINARY, OperatorType.PREFIX
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
    NOT = "not", OperatorType.PREFIX

    # Bitwise Operators
    BIN_LEFT = "<<"
    BIN_RIGHT = ">>"
    BIN_ZERO_RIGHT = ">>>"
    BIN_OR = "||"
    BIN_XOR = "^"
    BIN_AND = "&&"
    BIN_NOT = "~", OperatorType.PREFIX

    # Miscellaneous Operators
    SPREAD = "...", OperatorType.PREFIX
    RANGE = "..", OperatorType.BINARY, OperatorType.POSTFIX
    INC_RANGE = "..="
    COALESCE = "??"
    IN = "in"
    PATTERN_OR = "|"
    COLON = ":"

    # Assignment Operators
    ASSIGN = "=", OperatorType.ASSIGNMENT
    PLUS_ASSIGN = "+=", OperatorType.ASSIGNMENT
    MINUS_ASSIGN = "-=", OperatorType.ASSIGNMENT
    MULT_ASSIGN = "*=", OperatorType.ASSIGNMENT
    DIVIDE_ASSIGN = "/=", OperatorType.ASSIGNMENT
    EXPONENT_ASSIGN = "**=", OperatorType.ASSIGNMENT
    MOD_ASSIGN = "%=", OperatorType.ASSIGNMENT
    COALESCE_ASSIGN = "??=", OperatorType.ASSIGNMENT

    # Bitwise Assignment Operators
    BIN_LEFT_ASSIGN = "<<=", OperatorType.ASSIGNMENT
    BIN_RIGHT_ASSIGN = ">>=", OperatorType.ASSIGNMENT
    BIN_ZERO_RIGHT_ASSIGN = ">>>=", OperatorType.ASSIGNMENT
    BIN_OR_ASSIGN = "||=", OperatorType.ASSIGNMENT
    BIN_XOR_ASSIGN = "^=", OperatorType.ASSIGNMENT
    BIN_AND_ASSIGN = "&&=", OperatorType.ASSIGNMENT

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls)
        if args:
            obj._operator_types_ = args
        else:
            obj._operator_types_ = [OperatorType.BINARY]
        obj._value_ = value
        return obj
    
    @classmethod
    def _missing_(cls, value):
        return False

    @property
    def is_binary(self):
        return OperatorType.BINARY in self._operator_types_

    @property
    def is_postfix(self):
        return OperatorType.POSTFIX in self._operator_types_

    @property
    def is_prefix(self):
        return OperatorType.PREFIX in self._operator_types_

    @property
    def is_assignment(self):
        return OperatorType.ASSIGNMENT in self._operator_types_


class Keyword(StrEnum):
    # Declarations
    FUNCTION = "fn"
    GENERATOR = "gn"
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
    STEP = "step"
    WHILE = "while"
    LOOP = "loop"

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
    EXCLAMATION = "!"
    COMMA = ","
    FROM = "from"

    # Planned Features
    # TODO Slice Syntax for arrays, Destructuring assignment syntax
    _SWITCH = "switch"
    _CASE = "case"
    _MATCH = "match"

    _ARGUMENTS = "arguments"
    _ASYNC = "async"
    _AWAIT = "await"
    _ENUM = "enum"

    _IMPORT = "import"
    _EXPORT = "export"

    _CLASS = "class"
    STATIC = "stat"

    # Reserved (Not in use)
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

    @classmethod
    def _missing_(cls, value):
        return False


class CodeDelimiter(StrEnum):
    O_PAREN = "("
    C_PAREN = ")"
    O_BRACE = "{"
    C_BRACE = "}"
    O_BRACKET = "["
    C_BRACKET = "]"

    @classmethod
    def _missing_(cls, value):
        return False


class TextDelimiter(StrEnum):
    FORMAT_STRING = '"'
    PLAIN_STRING = "'"
    REGEX_STRING = "`"
    SINGLE_COMMENT_START = "//"
    SINGLE_COMMENT_END = "\n"
    MULTI_COMMENT_START = "/*"
    MULTI_COMMENT_END = "*/"

    @classmethod
    def _missing_(cls, value):
        return False


TEMPLATE_ARGUMENT_START = "${"
TEMPLATE_ARGUMENT_END = "}"
REGEX_FLAGS = ["d", "g", "i", "m", "s", "u", "y"]


class Formats:
    IDENTIFIER_REGEX = re.compile(r"(?!^_$)^[a-zA-Z_]+\w*$")
    is_identifier = lambda string: Formats.IDENTIFIER_REGEX.search(string) is not None

    FLOAT_INT_REGEX = re.compile(r"^(?!^0[^.eE])((\d+(\.\d*)?)|(\.\d+))([eE][+-]?\d+)?$")
    is_float_int = lambda string: Formats.FLOAT_INT_REGEX.search(string) is not None

    BIGINT_REGEX = re.compile(r"^(0|([1-9]+\d*))n$")
    is_bigint = lambda string: Formats.BIGINT_REGEX.search(string) is not None

    HEX_REGEX = re.compile(r"^0[xX][0-9a-fA-F]+n?$")
    is_hex = lambda string: Formats.HEX_REGEX.search(string) is not None

    OCTAL_REGEX = re.compile(r"^0[oO][0-7]+n?$")
    is_octal = lambda string: Formats.OCTAL_REGEX.search(string) is not None

    BINARY_REGEX = re.compile(r"^0[bB][01]+n?$")
    is_binary = lambda string: Formats.BINARY_REGEX.search(string) is not None


    # NOTE Doesn't work correctly...
    ESCAPE_SEQUENCE_REGEX = re.compile(
        r"^([0'\"\\nrvtbf]|(u[0-9a-fA-F]{4})|u{[0-9a-fA-F]{1,6}}|x[0-9a-fA-F]{2})"
    )
    is_valid_escape_sequence = (
        lambda string: Formats.ESCAPE_SEQUENCE_REGEX.search(string) is not None
    )

    @classmethod
    def is_number(cls, string: str):
        return (cls.is_float_int(string) or cls.is_bigint(string) or 
            cls.is_hex(string) or cls.is_octal(string) or cls.is_binary(string))
