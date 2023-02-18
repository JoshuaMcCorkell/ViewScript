from lex_data import (
    Operator,
    OperatorType,
    Keyword,
    CodeDelimiter,
    TextDelimiter,
    Formats,
    TEMPLATE_ARGUMENT_END,
    TEMPLATE_ARGUMENT_START,
    REGEX_FLAGS,
    letters,
    digits,
    reg_chars,
    whitespace,
    symbols,
)
from syntax_error import SyntaxError
from enum import Enum
from dataclasses import dataclass
from typing import List
import sys


class TokenType(Enum):
    OPERATOR = 0
    KEYWORD = 1
    CODE_DELIMITER = 2
    IDENTIFIER = 3

    NUMBER = 10
    PLAIN_STRING = 11
    FORMAT_STRING = 12
    REGEX_STRING = 13

    SINGLE_LINE_COMMENT = 20
    MULTI_LINE_COMMENT = 21

    ERROR = -1


class CharStream:
    def __init__(self, string: str):
        self.string = string
        self.index = 0

    def advance_next(self):
        self.index += 1
        if self.index < len(self.string):
            return self.string[self.index-1]
        else:
            raise IndexError("Char Stream is finished")
    
    def peak(self, offset: int):
        return self.string[self.index+offset]


@dataclass
class Token:
    type: TokenType
    name: Operator | Keyword | CodeDelimiter | str
    start: int
    end: int


def number(start_char: str, chars: CharStream) -> Token:
    pass


def lex(code: str) -> List[Token]:
    tokens = []
    chars = CharStream(code)
    while True:
        char = chars.advance_next()
        if char in digits:
            tokens.append(number(char, chars))
            #TODO



    return tokens
