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
    BUILT_IN_FUNCTIONS = {
        'print': [((_,), lambda obj: print(obj))],
    }

    def __init__(self, machine: "SimpleMachine", parent=None, args: List[Tuple]=None):
        self._patterns: Dict[str, List[Tuple[Tuple, FunctionType]]] = {}
        """
        프로시저들의 패턴매칭을 위한 테이블.
        do a b = plus a b
        do 1 b = 1
        do a 2 = 2
        do 3 3 = 10 이라면
        _patterns['do'] = [
            (1, _), lambda a, b: 1,
            (_, 2), lambda a, b: 2,
            (3, 3), lambda a, b: 10,
            (_, _), lambda a, b: plus(a, b)
        ]
        식으로 테이블에 저장되어야 하며, 순서는 함수의 선언 순서 그대로이다.
        호출시 탐색 순서는 차례대로가 된다.
        """
        self.machine = machine

        self._parent = parent
        if parent is None:
            self.init_built_ins()
        if args is not None:
            for arg in args:
                self._add(arg[0], None, arg[1])

    def init_built_ins(self):
        for key in SymbolTable.BUILT_IN_FUNCTIONS.keys():
            self._patterns[key] = SymbolTable.BUILT_IN_FUNCTIONS[key]

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
                pattern_params.append(self.machine.visit_literal(param))

        def function(*params): return self.machine.visit(value)
        self._add(name, pattern_params, function)

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
        if name in self._patterns:
            patts = self._patterns[name]
            if patts[0] is None:
                return patts[0][1](*params)
            if len(params) == 0:
                if len(patts) == 0:
                    return patts[0][1]()
                else:
                    def inner(*inner_params):
                        return patts[0][1](*inner_params)
                    return inner
            params_val = [self.machine.visit(p)() for p in params[0]]
            i = -1
            for pat in patts:
                i += 1
                if len(pat[0]) < len(params):
                    continue
                elif len(pat[0]) == len(params):
                    if SymbolTable.is_match(pat[0], params_val):
                        return patts[i][1](*params_val)
                elif len(pat[0]) > len(params):
                    if SymbolTable.is_match(pat[0][:len(params)], params_val):
                        def inner(*inner_params):
                            return pat[1](*params_val, *inner_params)
                        return inner

        if self._parent is not None:
            return self._parent.get(name, *params)

        raise TypeError('매칭되는 타입이 없음')


class SimpleMachine(BasicMachine):
    def __init__(self, code):
        self.tree = parse(code)
        self._table = SymbolTable(self)

    def run(self):
        for node in self.tree.nodes:
            self.visit(node)

    def visit(self, node: Node.Node):
        if isinstance(node, Node.FunctionNode):
            return self.visit_function(node)
        if isinstance(node, Node.AssignNode):
            self.visit_assign(node)
        if isinstance(node, Node.ValueNode):
            return self.visit_value(node)

    def visit_assign(self, node: Node.AssignNode):
        # define val var로 변경하는 신때틱 슈거이면 더 괜찮다고 생각.
        # 지금은 add과 set의 차이는 없지만, 나중에 설정해야 함.
        self._table.add_node(node.var, node.val)

    def visit_function(self, node: Node.FunctionNode):
        args = [(p, self.visit(p)) for p in node.params[1:]]
        scoped = SymbolTable(self, self._table, args)
        return scoped.get(node.params[0].tok, node.params[1:])

    def visit_value(self, node: Node.ValueNode):
        if isinstance(node, Node.Literal):
            return self.visit_literal(node)
        elif isinstance(node, Node.Identifier):
            return self.visit_id(node)
        elif isinstance(node, Node.WildCard):
            return _

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
        return self._table.get(node.tok)


def main():
    machine = SimpleMachine('''
        a = "!",
        b = 1,
        print a,
        print b
        ''')
    machine.run()
    print('ran!')

if __name__ == '__main__':
    main()
