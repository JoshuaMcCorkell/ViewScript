class SyntaxError(Exception):
    def __init__(self, message: str, line: int, *args):
        self.message = message
        self.line = line
        super(SyntaxError, self).__init__(message + "\nLine: " + str(line), *args)
