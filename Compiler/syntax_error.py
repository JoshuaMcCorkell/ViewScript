class SyntaxError(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        super(SyntaxError, self).__init__(*args)
