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

    @property
    def empty(self):
        return len(self._toks) <= 1

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
            self.check_pop('=')
            r = self.parse_value()
            if not self.empty:
                self.check_pop(',')
            return Node.AssignNode(l, r)
        if not self.empty:
            self.check_pop(',')
        return l

    def parse_value(self) -> Node.ValueNode:
        if self.top.is_literal():
            return self.parse_literal()
        return self.parse_function()

    def parse_function(self) -> Node.FunctionNode:
        res = []
        while not self.empty \
                and self.top.type not in [TokenType.COMMA, TokenType.EQUAL, TokenType.RBRAKET]:
            if self.top.type == TokenType.LBRAKET:
                self.check_pop('(')
                res.append(self.parse_value())
                self.check_pop(')')
            elif self.top.is_literal():
                res.append(self.parse_literal())
            else:
                res.append(Node.Identifier(self.pop().code))
        return Node.FunctionNode(res)

    def parse_literal(self) -> Node.Literal:
        return Node.Literal(self.pop())


def main():
    b = Builder(open('code.txt', encoding='utf-8').read())
    res = b.parse()
    print('parsed!')

if __name__ == '__main__':
    main()
