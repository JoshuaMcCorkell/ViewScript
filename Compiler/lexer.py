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
        self._next_index_ = 0

    def advance_next(self):
        self._next_index_ += 1
        if self._next_index_ < len(self.string):
            return self.string[self._next_index_ - 1]
        else:
            raise IndexError("Char Stream is finished")

    def peak(self, offset: int):
        return self.string[self._next_index_ + offset]

    @property
    def next_index(self):
        return self._next_index_


@dataclass
class Token:
    type: TokenType
    name: Operator | Keyword | CodeDelimiter | str
    start: int
    end: int


def number(chars: CharStream) -> Token:
    start = chars.next_index - 1
    token = chars.peak(-1)
    while True:
        char = chars.peak(1)
        if char in reg_chars:
            token += chars.advance_next()
        elif char in [Operator.PLUS.value, Operator.MINUS.value] and chars.peak(-1) in ["e", "E"]:
                token += chars.advance_next()
        else:
            break
    if Formats.is_number(token):
        return Token(TokenType.NUMBER, token, start, chars.next_index-1)
    else:
        raise SyntaxError(f"Invalid Number Literal {token}.")


def word(chars: CharStream) -> Token:
    start = chars.next_index - 1
    token = chars.peak(-1)
    while True:
        char = chars.peak(1)
        if char in reg_chars:
            token += chars.advance_next()
        else:
            break
    end = chars.next_index - 1
    if Operator(token):
        return Token(TokenType.OPERATOR, Operator(token), start, end)
    elif Keyword(token):
        return Token(TokenType.Keyword, Keyword(token), start, end)
    else:
        return Token(TokenType.IDENTIFIER, token, start, end)


def symbol(chars: CharStream) -> Token:
    start = chars.next_index - 1
    token = chars.peak(-1)
    while True:
        char = chars.peak(1)
        if char in symbols:
            token += chars.advance_next()
        else:
            break
    end = chars.next_index - 1
    if Operator(token):
        return Token(TokenType.OPERATOR, Operator(token), start, end)
    elif Keyword(token):
        return Token(TokenType.Keyword, Keyword(token), start, end)
    elif CodeDelimiter(token):
        return Token(TokenType.CODE_DELIMITER, CodeDelimiter(token), start, end)
    else:
        raise SyntaxError(f"Invalid Operator/Symbol {token}.")


def single_line_comment(chars: CharStream) -> Token:
    pass


def multi_line_comment(chars: CharStream) -> Token:
    pass


def string(chars: CharStream) -> Token:
    pass


def regex(chars: CharStream) -> Token:
    pass


def text(chars: CharStream) -> Token:
    pass


def lex(code: str) -> List[Token]:
    tokens = []
    chars = CharStream(code)
    while True:
        try:
            char = chars.advance_next()
        except IndexError:
            break
        if char in digits:
            tokens.append(number(chars))
        elif char in reg_chars:
            tokens.append(word(chars))
        elif TextDelimiter(char) or TextDelimiter(char + chars.peak(1)):
            tokens.append(text(chars))
        elif char in symbols:
            tokens.append(symbol(chars))
        elif char in whitespace:
            continue
        else:
            raise SyntaxError(f"Invalid Character {char}.")

    return tokens
