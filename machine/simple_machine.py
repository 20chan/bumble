from machine.basic_machine import BasicMachine
from parse.builder import parse
from parse.AST import Node
from parse.tok import Token, TokenType


class SymbolTable:
    def __init__(self):
        self._table = {}

    def add(self, val: Node.FunctionNode, var):
        self._table[val] = var

    def __getitem__(self, item):
        return self._table[item]


class SimpleMachine(BasicMachine):
    def __init__(self, code):
        self.tree = parse(code)
        self._table = SymbolTable()

    def run(self):
        self.visit(self.tree)

    def visit(self, node: Node.Node):
        if isinstance(node, Node.FunctionNode):
            self.visit_function(node)

    def visit_assign(self, node: Node.AssignNode):
        # define val var로 변경하는 신태틱 슈거이면 더 괜찮다고 생각.
        self._table.add(node.val, self.visit(node.var))

    def visit_function(self, node: Node.FunctionNode):
        pass

    def visit_value(self, node: Node.ValueNode):
        if isinstance(node, Node.Literal):
            return self.visit_literal(node)
        elif isinstance(node, Node.Identifier):
            return self.visit_id(node)

    def visit_literal(self, node: Node.Literal):
        if node.type == TokenType.INTEGER:
            return int(node.tok)
        if node.type == TokenType.REAL:
            return float(node.tok)
        if node.type == TokenType.STRING:
            return str(node.tok)
        if node.type == TokenType.CHAR:
            return str(node.tok)
        if node.type == TokenType.TRUE:
            return True
        if node.type == TokenType.FALSE:
            return False

        raise TypeError

    def visit_id(self, node: Node.Identifier):
        return self._table[node.tok]
