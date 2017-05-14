from machine.basic_machine import BasicMachine
from parse.builder import parse
from parse.AST import Node
from parse.tok import Token, TokenType
from typing import Dict, Tuple, List
from types import FunctionType


class Wildcard:
    pass

_ = Wildcard()


class SymbolTable:

    def __init__(self, machine: "SimpleMachine", parent=None, args: List[Tuple]=None):
        self._patterns: Dict[str, List[Tuple[Tuple, Node.ValueNode]]] = {}
        """
        프로시저들의 패턴매칭을 위한 테이블.
        do a b = plus a b
        do 1 b = 1
        do a 2 = 2
        do 3 3 = 10 이라면
        _patterns['do'] = [
            (1, _), Node.ValueNode,
            (_, 2), Node.ValueNode,
            (3, 3), Node.ValueNode,
            (_, _), Node.ValueNode
        ]
        식으로 테이블에 저장되어야 하며, 순서는 함수의 선언 순서 그대로이다.
        호출시 탐색 순서는 차례대로가 된다.
        
        빌트인 함수는 callable 객체로 저장을 한다.
        즉, callable하면 그냥 call하면 되고 노드이면 visit하면 됨
        """
        self.machine = machine

        self.parent = parent
        if parent is None:
            self.init_built_ins()
        if args is not None:
            for arg in args:
                self._add(arg[0], None, arg[1])

    def init_built_ins(self):
        # 아무래도 테이블 구조를 바꿔야 겠음. 함수가 아닌 노드로 값을 바꿔야 더 유연해질 거 같음
        builtin_functions = {
            'print': [((_,), lambda obj: print(obj))],
            'plus': [((_, _), lambda a, b: a+b)],
        }
        for key in builtin_functions.keys():
            self._patterns[key] = builtin_functions[key]

    def _add(self, name, pat, function):
        if name in self._patterns:
            self._patterns[name].append((pat, function))
        else:
            self._patterns[name] = [(pat, function)]

    def add_node(self, var: Node.FunctionNode, value: Node.ValueNode):
        name = var.params[0].tok
        pattern_params = []
        for param in var.params[1:]:
            if isinstance(param, Node.Identifier) or isinstance(param, Node.WildCard):
                pattern_params.append(_)
            elif isinstance(param, Node.Literal):
                pattern_params.append(self.machine.visit_literal(param, self))

        self._add(name, pattern_params, value)

    @staticmethod
    def is_match(pattern, params):
        matched = True
        i = 0
        for pat_cond in pattern:  # 패턴이 매칭되는지 확인
            if not (pat_cond == _ or pat_cond == params[i]):
                matched = False
                break
            i += 1
        return matched

    def get(self, name, *params):
        # 일단 커링은 생각하지 않고 만들어보자!
        if callable(self._patterns[name][0][1]):
            return self._patterns[name][0][1](*params)
        return self.machine.visit(self._patterns[name][0][1], self)


class SimpleMachine(BasicMachine):
    def __init__(self, code):
        self.tree = parse(code)
        # self._table = SymbolTable(self)

    def run(self):
        table = SymbolTable(self)
        for node in self.tree.nodes:
            self.visit(node, table)

    def visit(self, node: Node.Node, table: SymbolTable):
        if isinstance(node, Node.FunctionNode):
            return self.visit_function(node, table)
        if isinstance(node, Node.AssignNode):
            self.visit_assign(node, table)
        if isinstance(node, Node.ValueNode):
            return self.visit_value(node, table)

    def visit_assign(self, node: Node.AssignNode, table: SymbolTable):
        # define val var로 변경하는 신때틱 슈거이면 더 괜찮다고 생각.
        # 지금은 add과 set의 차이는 없지만, 나중에 설정해야 함.
        table.add_node(node.var, node.val)

    def visit_function(self, node: Node.FunctionNode, table: SymbolTable):
        # name = node.params[0].tok
        # args = [(p, self.visit(p, table)) for p in node.params[1:]]
        # new_table = SymbolTable(self, table, args)
        args = [self.visit(p, table) for p in node.params[1:]]
        res = table.get(node.params[0].tok, *args)
        return res

    def visit_value(self, node: Node.ValueNode, table: SymbolTable):
        if isinstance(node, Node.Literal):
            return self.visit_literal(node, table)
        elif isinstance(node, Node.Identifier):
            return self.visit_id(node, table)
        elif isinstance(node, Node.WildCard):
            return _

    def visit_literal(self, node: Node.Literal, table: SymbolTable):
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

    def visit_id(self, node: Node.Identifier, table: SymbolTable):
        return table.get(node.tok)


def main():
    machine = SimpleMachine('''
        a = 1,
        print a
        ''')
    machine.run()
    print('ran!')

if __name__ == '__main__':
    main()
