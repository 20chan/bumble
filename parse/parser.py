from parse.lexer import tokenize
from parse.tok import TokenType
import parse.AST.Node as Node


class Parser:
    def __init__(self, code: str):
        self.code = code
        self.lex = iter(tokenize(code))
        self.current_tok = next(self.lex)

    def next_tok(self):
        self.current_tok = next(self.lex)
        return self.current_tok

    def parse(self) -> Node.Node:
        return self.parse_sentence()

    def parse_sentence(self) -> Node.Sentence:
        if self.next_tok().TokenType == TokenType.IF:
            return self.parse_if()
        if self.next_tok().TokenType == TokenType.WHILE:
            return self.parse_while()
        if self.next_tok().TokenType == TokenType.FOR:
            return self.parse_for()
        if self.next_tok().TokenType == TokenType.COND:
            return self.parse_cond()
        if self.next_tok().TokenType == TokenType.MATCH:
            return self.parse_match()
        if self.next_tok().TokenType == TokenType.TRY:
            return self.parse_try()
        if self.next_tok().TokenType == TokenType.ENUM:
            return self.parse_enum()
        if self.next_tok().TokenType == TokenType.CLASS:
            return self.parse_class()
        if self.next_tok().TokenType == TokenType.FUNC:
            return self.parse_func()
        if self.next_tok().TokenType == TokenType.VAR:
            return self.parse_var()
        if self.next_tok().TokenType == TokenType.IDENTIFIER:



    def parse_block(self) -> [Node.Sentence]:
        res = []
        while self.next_tok() != "}":
            res.append(self.parse_sentence())
        return res

    def parse_statement(self) -> Node.Statement:
        if self.next_tok().code == "{":
            return Node.Statement(self.parse_block())
        else:
            return Node.Statement(self.parse_sentence())

    def parse_if(self):
        cond = self.parse_expr()
        true_block = self.parse_statement()

        if self.next_tok().TokenType == TokenType.ELSE:
            false_block = self.parse_statement()
        else:
            false_block = None

        return Node.StateIf(cond, true_block, false_block)

    def parse_expr(self) -> Node.Expression:
        pass
