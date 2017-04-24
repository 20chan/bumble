from parse.tok import Token, TokenType
from parse.lexer import tokenize
from parse.AST import Node


class Builder:
    def __init__(self, code: str):
        self._toks = list(tokenize(code))

    def pop(self):
        return self._toks.pop(0)

    @property
    def top(self):
        return self._toks[0]

    def check_pop(self, tok):
        assert(self.pop().code == tok)

    def parse(self) -> Node.ProgramNode:
        res = []
        while self.top.type != TokenType.EOF:
            res.append(self.parse_statement())

        return Node.ProgramNode(res)

    def parse_statement(self) -> Node.Node:
        l = self.parse_function()
        if self.top.type == TokenType.EQUAL:
            r = self.parse_value()
            return Node.AssignNode(l, r)
        return l

    def parse_value(self) -> Node.ValueNode:
        if self.top.is_literal():
            return self.parse_literal()

    def parse_function(self) -> Node.FunctionNode:
        pass

    def parse_literal(self) -> Node.Literal:
        return Node.Literal(self.pop())
