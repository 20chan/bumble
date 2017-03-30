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

    def check_pop(self, tok):
        return self.pop_tok().code == tok

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
        self.check_pop('{')
        while self.top != "}":
            res.append(self.parse_sentence())
        self.check_pop('}')
        return res

    def parse_statement(self) -> Node.Statement:
        if self.top.code == "{":
            return Node.Statement(self.parse_block())
        else:
            return Node.Statement(self.parse_sentence())

    def parse_if(self) -> Node.StateIf:
        self.check_pop('if')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        true_block = self.parse_statement()

        if self.pop_tok().TokenType == TokenType.ELSE:
            false_block = self.parse_statement()
        else:
            false_block = None

        return Node.StateIf(cond, true_block, false_block)

    def parse_while(self) -> Node.StateWhile:
        self.check_pop('while')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        block = self.parse_statement()

        return Node.StateWhile(cond, block)

    def parse_for(self) -> Node.StateFor:
        self.check_pop('for')
        self.check_pop('(')
        init = self.parse_expr()
        check = self.parse_expr()
        add = self.parse_expr()
        block = self.parse_statement()

        return Node.StateFor(init, check, add, block)

    def parse_cond(self) -> Node.StateCond:
        self.check_pop('cond')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        self.check_pop('{')
        states = []
        other = None
        while self.top.code != '}':
            pat = self.parse_pattern()
            self.check_pop('then')
            stmt = self.parse_statement()
            states.append((pat, stmt))
        if self.top.code == 'otherwise':
            self.check_pop('otherwise')
            other = self.parse_expr()
        self.check_pop('}')

        return Node.StateCond(cond, states, other)

    def parse_match(self) -> Node.StateMatch:
        self.check_pop('match')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        self.check_pop('{')
        states = []
        while self.top.code != '}':
            pat = self.parse_pattern()
            self.check_pop('then')
            stmt = self.parse_statement()
            states.append((pat, stmt))

        return Node.StateMatch(cond, states)

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
