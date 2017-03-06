from parse import AST
from parse.lexer import tokenize
from parse.tok import TokenType


class Parser:
    def __init__(self, code: str):
        self.code = code
        self.lex = iter(tokenize(code))
        self.current_tok = next(self.lex)

    @staticmethod
    def error():
        raise Exception('Invalid syntax')

    def eat(self, tok_type: TokenType):
        if self.current_tok == tok_type:
            self.current_tok = next(self.lex)
        else:
            Parser.error()

    def parse(self) -> AST.AST:
        node = self.sentence()
        try:
            while True:
                self.sentence()
        except StopIteration:
            return node

    def sentence(self) -> AST.AST:
        pass
