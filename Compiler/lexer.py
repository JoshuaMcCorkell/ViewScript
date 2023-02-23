from lex_data import (
    TokenType,
    Operator,
    OperatorType,
    Keyword,
    CodeDelimiter,
    StringDelimiter,
    Comment,
    Formats,
    TEMPLATE_ARGUMENT_END,
    TEMPLATE_ARGUMENT_START,
    REGEX_FLAGS,
    letters,
    digits,
    reg_chars,
    whitespace,
    symbols,
    escape_char,
)
from syntax_error import SyntaxError
from enum import Enum
from dataclasses import dataclass
from typing import List


quote_types = set(item.value for item in StringDelimiter)
comment_starters = set(item.start for item in Comment)
code_delimiters = set(item.value for item in CodeDelimiter)


class EOFException(Exception):
    pass


class CharStream:
    def __init__(self, string: str):
        self.string = string
        self._current_index = -1
        self._line_number = 1

    def advance_next(self):
        self._current_index += 1
        if self._current_index < len(self.string):
            if self.string[self._current_index] == "\n":
                self._line_number += 1
            return self.string[self._current_index]
        else:
            raise EOFException("Unexpected EOF (End of File)")

    def peak(self, offset: int):
        try:
            return self.string[self._current_index + offset]
        except IndexError:
            raise EOFException("Unexpected EOF (End of File)")

    @property
    def current_index(self):
        return self._current_index

    @property
    def line_number(self):
        return self._line_number

    def start_token(self):
        return self._current_index, self._line_number, self.peak(0)


@dataclass
class Token:
    type: TokenType
    name: Operator | Keyword | CodeDelimiter | str
    line: int
    start: int
    end: int


class Lexer:
    def number(self, chars: CharStream) -> Token:
        start, line, token = chars.start_token()
        has_dot = (token == ".")
        while True:
            try:
                char = chars.peak(1)
                if char in reg_chars:
                    token += chars.advance_next()
                elif char in [Operator.PLUS.value, Operator.MINUS.value] and chars.peak(
                    -1
                ) in ["e", "E"]:
                    token += chars.advance_next()
                elif char == "." and not has_dot:
                    token += chars.advance_next()
                    has_dot = True
                else:
                    break
            except EOFException:
                break
        if Formats.is_number(token):
            return Token(TokenType.NUMBER, token, line, start, chars.current_index - 1)
        else:
            raise SyntaxError(f"Invalid Number Literal {token}", line)


    def word(self, chars: CharStream) -> Token:
        start, line, token = chars.start_token()
        while True:
            try:
                char = chars.peak(1)
                if char in reg_chars:
                    token += chars.advance_next()
                else:
                    break
            except EOFException:
                break
        end = chars.current_index - 1
        if token in set(item.value for item in Operator):
            return Token(TokenType.OPERATOR, Operator(token), line, start, end)
        elif token in set(item.value for item in Keyword):
            return Token(TokenType.KEYWORD, Keyword(token), line, start, end)
        else:
            return Token(TokenType.IDENTIFIER, token, line, start, end) 


    def symbol(self, chars: CharStream) -> Token:
        start, line, token = chars.start_token()
        if token == "." and Formats.is_number((token + chars.peak(1))):
            return self.number(chars)
        if token in code_delimiters:
            return Token(TokenType.CODE_DELIMITER, CodeDelimiter(token), line, start, chars.current_index - 1)
        while True:
            try:
                char = chars.peak(1)
                if char in symbols:
                    token += chars.advance_next()
                else:
                    break
            except EOFException:
                break
        end = chars.current_index - 1
        if token in set(item.value for item in Operator):
            return Token(TokenType.OPERATOR, Operator(token), line, start, end)
        elif token in set(item.value for item in Keyword):
            return Token(TokenType.KEYWORD, Keyword(token), line, start, end)
        else:
            raise SyntaxError(f"Invalid Operator/Symbol {token}", line)


    def comment(self, comment_type: Comment, chars: CharStream) -> Token:
        start, line, token = chars.start_token()
        while True:
            try:
                token += chars.advance_next()
                if token[-1] == comment_type.end:
                    break
            except EOFException:
                break
        return Token(comment_type.token_type, token, line, start, chars.current_index - 1)


    def string(self, chars: CharStream) -> Token:
        _, _, token = chars.start_token()
        if token == StringDelimiter.PLAIN_STRING.value:
            return self.plain_string(chars)
        elif token == StringDelimiter.FORMAT_STRING.value:
            return self.format_string(chars)
        elif token == StringDelimiter.REGEX_STRING.value:
            return self.regex(chars)


    def regex(self, chars: CharStream) -> Token:
        start, line, _ = chars.start_token()
        token = chars.peak(0)
        while True:
            try:
                char = chars.peak(1)
                if char == StringDelimiter.REGEX_STRING.value:
                    chars.advance_next()
                    break
                elif (
                    char == escape_char
                    and chars.peak(2) == StringDelimiter.REGEX_STRING.value
                ):
                    token += StringDelimiter.REGEX_STRING.value
                elif char == "/":
                    token += "\/"
                else:
                    token += chars.advance_next()
            except EOFException:
                raise SyntaxError(f"Unterminated Regex Literal {token}", line)
        current_regex_flags = []
        while True:
            try:
                char = chars.peak(1)
                if char in REGEX_FLAGS and char not in current_regex_flags:
                    token += chars.advance_next()
                    current_regex_flags.append(token[-1])
                elif char in letters:
                    raise SyntaxError(f"Invalid Regex Flags: {current_regex_flags}")
                else:
                    break     
            except EOFException:
                break
        return Token(TokenType.REGEX_STRING, token, line, start, chars.current_index - 1)


    def plain_string(self, chars: CharStream) -> Token:
        start, line, _ = chars.start_token()
        token = chars.peak(0)
        while True:
            try:
                char = chars.peak(1)
                if char == StringDelimiter.PLAIN_STRING.value:
                    token += chars.advance_next()
                    break
                elif char == escape_char:
                    token += chars.advance_next() + chars.advance_next()
                else:
                    token += chars.advance_next()
            except EOFException:
                raise SyntaxError(f"Unterminated String Literal {token}", line)
        return Token(TokenType.PLAIN_STRING, token, line, start, chars.current_index - 1)


    def format_string(self, chars: CharStream) -> Token:
        # TEMPORARY
        return self.plain_string(chars)


    def lex(self, *, code_string: str="", char_stream: CharStream=None) -> List[Token]:
        try:
            tokens = []
            if char_stream is None:
                chars = CharStream(code_string)
            else:
                chars = char_stream
            while True:
                try:
                    char = chars.advance_next()
                except EOFException:
                    break
                try:
                    char_plus = None
                    char_plus = char + chars.peak(1)
                    char_plus_plus = char_plus + chars.peak(2)
                except EOFException:
                    if char_plus is not None:
                        char_plus_plus = char_plus
                    else:
                        char_plus_plus = char_plus = char

                if char in digits:
                    tokens.append(self.number(chars))
                elif char in quote_types:
                    tokens.append(self.string(chars))
                elif char in comment_starters:
                    tokens.append(self.comment(Comment(char), chars))
                elif char_plus in comment_starters:
                    tokens.append(self.comment(Comment(char + chars.peak(1)), chars))
                elif char_plus_plus in comment_starters:
                    tokens.append(
                        self.comment(Comment(char + chars.peak(1) + chars.peak(2)), chars)
                    )
                elif char in reg_chars:
                    tokens.append(self.word(chars))
                elif char in symbols:
                    tokens.append(self.symbol(chars))
                elif char in whitespace:
                    continue
                else:
                    raise SyntaxError(f"Invalid Character {char}", chars.line_number)
            return tokens
        except SyntaxError as e:
            tokens.append(e)
            return tokens


def command_line():
    import sys
    code = open(sys.argv[1]).read()
    print(code)
    print("\n", *Lexer().lex(code_string=code), sep="\n")


if __name__ == "__main__":
    command_line()
