from parse.lexer import tokenize
from parse.tok import Token, TokenType
import parse.AST.Node as Node


class Parser:
    def __init__(self, code: str):
        self.code = code
        self._toks = list(tokenize(code))

    def pop_tok(self):
        return self._toks.pop()

    @property
    def top(self) -> Token:
        return self._toks[0]

    def parse(self) -> Node.Node:
        return self.parse_sentence()

    def parse_sentence(self) -> Node.Sentence:
        if self.top.type == TokenType.IF:
            return self.parse_if()
        if self.top.type == TokenType.WHILE:
            return self.parse_while()
        if self.top.type == TokenType.FOR:
            return self.parse_for()
        if self.top.type == TokenType.COND:
            return self.parse_cond()
        if self.top.type == TokenType.MATCH:
            return self.parse_match()
        if self.top.type == TokenType.TRY:
            return self.parse_try()
        if self.top.type == TokenType.ENUM:
            return self.parse_enum()
        if self.top.type == TokenType.CLASS:
            return self.parse_class()
        if self.top.type == TokenType.FUNC:
            return self.parse_func()
        if self.top.type == TokenType.VAR:
            return self.parse_var()
        if self.top.type == TokenType.IDENTIFIER:
            return self.parse_id()

    def parse_block(self) -> [Node.Sentence]:
        res = []
        while self.pop_tok() != "}":
            res.append(self.parse_sentence())
        return res

    def parse_statement(self) -> Node.Statement:
        if self.pop_tok().code == "{":
            return Node.Statement(self.parse_block())
        else:
            return Node.Statement(self.parse_sentence())

    def parse_if(self):
        cond = self.parse_expr()
        true_block = self.parse_statement()

        if self.pop_tok().TokenType == TokenType.ELSE:
            false_block = self.parse_statement()
        else:
            false_block = None

        return Node.StateIf(cond, true_block, false_block)

    def parse_expr(self) -> Node.Expression:
        pass

    def parse_id(self) -> Node.Expression:
        identifier = self.pop_tok()
        if self.top.code == '=':
            return self.parse_assign(identifier)
        if self.top.type == TokenType.BIND:
            return self.parse_bind(identifier)
        if self.top.code == '(':
            return self.parse_call(identifier)

    def parse_assign(self, ide) -> Node.NodeAssign:
        pass

    def parse_bind(self, ide) -> Node.NodeBind:
        pass

    def parse_call(self, ide) -> Node.NodeCall:
        pass
