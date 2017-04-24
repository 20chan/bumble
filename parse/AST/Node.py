from typing import List
from parse.tok import Token, TokenType


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes


class ValueNode(Node):
    pass


class FunctionNode(ValueNode):
    def __init__(self, params: List[ValueNode]):
        self.params = params


class AssignNode(Node):
    def __init__(self, var: FunctionNode, val: ValueNode):
        self.var = var
        self.val = val


class Literal(ValueNode):
    def __init__(self, tok: Token):
        self.tok = tok.code
        self.type = tok.type


class Identifier(ValueNode):
    def __init__(self, tok: str):
        self.tok = tok
