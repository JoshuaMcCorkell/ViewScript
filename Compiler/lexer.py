from lex_data import (
    TokenType,
    Operator,
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
from dataclasses import dataclass
from typing import Generator, List


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

    def __init__(self, *, code_string: str=None, char_stream: CharStream=None):
        if code_string is not None:
            self.chars = CharStream(code_string)
        elif char_stream is not None:
            self.chars = char_stream
        else:
            raise ValueError("code_string or char_stream argument must be passed with an argument of the correct type.")


    def number(self) -> Token:
        start, line, token = self.chars.start_token()
        has_dot = (token == ".")
        while True:
            try:
                char = self.chars.peak(1)
                if char in reg_chars:
                    token += self.chars.advance_next()
                elif char in [Operator.PLUS.value, Operator.MINUS.value] and self.chars.peak(
                    -1
                ) in ["e", "E"]:
                    token += self.chars.advance_next()
                elif char == "." and not has_dot:
                    token += self.chars.advance_next()
                    has_dot = True
                else:
                    break
            except EOFException:
                break
        if Formats.is_number(token):
            return Token(TokenType.NUMBER, token, line, start, self.chars.current_index - 1)
        else:
            raise SyntaxError(f"Invalid Number Literal {token}", line)


    def word(self) -> Token:
        start, line, token = self.chars.start_token()
        while True:
            try:
                char = self.chars.peak(1)
                if char in reg_chars:
                    token += self.chars.advance_next()
                else:
                    break
            except EOFException:
                break
        end = self.chars.current_index 
        if token in set(item.value for item in Operator):
            return Token(TokenType.OPERATOR, Operator(token), line, start, end)
        elif token in set(item.value for item in Keyword):
            return Token(TokenType.KEYWORD, Keyword(token), line, start, end)
        else:
            return Token(TokenType.IDENTIFIER, token, line, start, end) 


    def symbol(self) -> Token:
        start, line, token = self.chars.start_token()
        if token == "." and Formats.is_number((token + self.chars.peak(1))):
            return self.number()
        if token in code_delimiters:
            return Token(TokenType.CODE_DELIMITER, CodeDelimiter(token), line, start, self.chars.current_index - 1)
        while True:
            try:
                char = self.chars.peak(1)
                if char in symbols:
                    token += self.chars.advance_next()
                else:
                    break
            except EOFException:
                break
        end = self.chars.current_index
        if token in set(item.value for item in Operator):
            return Token(TokenType.OPERATOR, Operator(token), line, start, end)
        elif token in set(item.value for item in Keyword):
            return Token(TokenType.KEYWORD, Keyword(token), line, start, end)
        else:
            raise SyntaxError(f"Invalid Operator/Symbol {token}", line)


    def comment(self, comment_type: Comment) -> Token:
        start, line, token = self.chars.start_token()
        while True:
            try:
                token += self.chars.advance_next()
                if token[-1] == comment_type.end:
                    break
            except EOFException:
                break
        return Token(comment_type.token_type, token, line, start, self.chars.current_index - 1)


    def string(self) -> Token:
        _, _, token = self.chars.start_token()
        if token == StringDelimiter.PLAIN_STRING.value:
            return self.plain_string()
        elif token == StringDelimiter.TEMPLATE_STRING.value:
            return self.template_string()
        elif token == StringDelimiter.REGEX_STRING.value:
            return self.regex()


    def regex(self) -> Token:
        start, line, _ = self.chars.start_token()
        token = self.chars.peak(0)
        while True:
            try:
                char = self.chars.peak(1)
                if char == StringDelimiter.REGEX_STRING.value:
                    self.chars.advance_next()
                    break
                elif (
                    char == escape_char
                    and self.chars.peak(2) == StringDelimiter.REGEX_STRING.value
                ):
                    token += StringDelimiter.REGEX_STRING.value
                elif char == "/":
                    token += "\/"
                else:
                    token += self.chars.advance_next()
            except EOFException:
                raise SyntaxError(f"Unterminated Regex Literal {token}", line)
        current_regex_flags = []
        while True:
            try:
                char = self.chars.peak(1)
                if char in REGEX_FLAGS and char not in current_regex_flags:
                    token += self.chars.advance_next()
                    current_regex_flags.append(token[-1])
                elif char in letters:
                    raise SyntaxError(f"Invalid Regex Flags: {current_regex_flags}")
                else:
                    break     
            except EOFException:
                break
        return Token(TokenType.REGEX_STRING, token, line, start, self.chars.current_index - 1)


    def plain_string(self) -> Token:
        start, line, _ = self.chars.start_token()
        token = self.chars.peak(0)
        while True:
            try:
                char = self.chars.peak(1)
                if char == StringDelimiter.PLAIN_STRING.value:
                    token += self.chars.advance_next()
                    break
                elif char == escape_char:
                    token += self.chars.advance_next() + self.chars.advance_next()
                else:
                    token += self.chars.advance_next()
            except EOFException:
                raise SyntaxError(f"Unterminated String Literal {token}", line)
        return Token(TokenType.PLAIN_STRING, token, line, start, self.chars.current_index - 1)


    def template_string(self) -> Token:
        start, line, _ = self.chars.start_token()
        token = self.chars.peak(0);
        template_arguments = {}
        while True:
            try:
                char = self.chars.peak(1)
                if char == StringDelimiter.TEMPLATE_STRING.value:
                    token += self.chars.advance_next()
                    break
                elif char == escape_char:
                    token += self.chars.advance_next() + self.chars.advance_next()
                elif char == "$":
                    token += "\\$"
                elif char == TEMPLATE_ARGUMENT_START.value:
                    # TODO This should be the position WITHIN the string that the argument starts.
                    # It gets thrown off when dealing with multiple arguments.
                    argument_start = self.chars.current_index - start  
                    self.chars.advance_next()
                    template_argument_tokens = []
                    open_braces = 1
                    token_stream = self.lex_stream()
                    while open_braces != 0:
                        next_token = next(token_stream)
                        if next_token.name == CodeDelimiter.O_BRACE:
                            open_braces += 1
                        elif next_token.name == CodeDelimiter.C_BRACE:
                            open_braces -= 1
                        if open_braces:
                            template_argument_tokens.append(next_token)
                    template_arguments[argument_start] = template_argument_tokens
                else:
                    token += self.chars.advance_next()

            except EOFException:
                raise SyntaxError("Unterminated Template String Literal.", line)
        return Token(TokenType.TEMPLATE_STRING, (token, template_arguments), line, start, self.chars.current_index - 1)

    def lex_stream(self) -> Generator:
        while True:
            try:
                char = self.chars.advance_next()
            except EOFException:
                return
            try:
                char_plus = None
                char_plus = char + self.chars.peak(1)
                char_plus_plus = char_plus + self.chars.peak(2)
            except EOFException:
                if char_plus is not None:
                    char_plus_plus = char_plus
                else:
                    char_plus_plus = char_plus = char

            if char in digits:
                yield self.number()
            elif char in quote_types:
                yield self.string()
            elif char in comment_starters:
                yield self.comment(Comment(char))
            elif char_plus in comment_starters:
                yield self.comment(Comment(char + self.chars.peak(1)))
            elif char_plus_plus in comment_starters:
                yield self.comment(Comment(char + self.chars.peak(1) + self.chars.peak(2)))
            elif char in reg_chars:
                yield self.word()
            elif char in symbols:
                yield self.symbol()
            elif char in whitespace:
                continue
            else:
                raise SyntaxError(f"Invalid Character {char}", self.chars.line_number)

    def lex(self) -> List[Token]:
        try:
            tokens = []
            for token in self.lex_stream():
                tokens.append(token)
            return tokens
        except SyntaxError as e:
            tokens.append(e)
            return tokens



def command_line():
    import sys
    code = open(sys.argv[1]).read()
    print("\n", *Lexer(code_string=code).lex(), sep="\n")


if __name__ == "__main__":
    command_line()
