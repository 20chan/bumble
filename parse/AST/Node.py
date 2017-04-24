from parse.tok import Token, TokenType


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class ValueNode(Node):
    pass


class FunctionNode(ValueNode):
    def __init__(self, function, params):
        self.function = function
        self.params = params


class AssignNode(Node):
    def __init__(self, var, val):
        self.var = var
        self.val = val


class Literal(ValueNode):
    def __init__(self, tok: Token):
        self.tok = tok.code
        self.type = tok.type
