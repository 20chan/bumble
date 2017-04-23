from parse.tok import Token, TokenType
from parse.lexer import tokenize
from parse.AST import Node


class Builder:
    def __init__(self, code: str):
        self.code = tokenize(code)

    def parse(self):
        raise NotImplementedError
