from parse.tok import Token, TokenType


class Node:
    pass


class FunctionNode(Node):
    def __init__(self, function, params):
        self.function = function
        self.params = params


class AssignNode(Node):
    def __init__(self, var, val):
        self.var = var
        self.val = val
