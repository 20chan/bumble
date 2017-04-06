from machine.basic_machine import Machine
from parse.tok import TokenType
from parse.AST import Node
from typing import Dict
from copy import deepcopy

# 이거 내일 일어나면 다 갈아 엎고 다시 짜자


class Object:
    def __init__(self, typ, value):
        self.type = typ
        self.value = value
        self.attrs: Dict[str, Variable] = typ.attrs

    def trailer_call(self, *args):
        return self.value(*args)

    def trailer_index(self, args):
        return self.attrs['get'].trailer_call(self, args)

    def trailer_dot(self, name):
        return self.attrs[name]


class Type(Object):
    types = []

    def __init__(self, name: str, attrs, parent=None):
        self.name = name
        self.attrs = dict()
        if parent is not None:
            self.attrs = parent.attrs
        for key in attrs.keys():
            self.attrs[key] = attrs[key]
        self.parent = parent
        Type.types.append(self)
        self.value = self
        Object.__init__(self, self, self)


class Variable(Object):
    def __init__(self, name: str, typ: Type, value):
        self.name = name
        Object.__init__(self, typ, value)

    def __repr__(self):
        return '{}: {}'.format(self.name, self.value)

    def trailer_call(self, parent, *args):
        return self.value(parent, *args)


class Literal(Object):
    def __init__(self, typ: Type, value):
        Object.__init__(self, typ, value)


class SimpleMachine(Machine):
    def __init__(self, global_vars):
        self.table = {}
        for gv in global_vars:
            self.table[gv.name] = gv

    def execute(self, node: Node.Statement):
        for s in node.sentences:
            self.visit(s)
        pass

    def visit(self, node: Node.Node):
        if isinstance(node, Node.StateImport):
            return self.visit_import(node)
        if isinstance(node, Node.NodeAssign):
            return self.visit_assign(node)
        if isinstance(node, Node.DefVar):
            return self.visit_def_var(node)
        if isinstance(node, Node.ExprOr):
            return self.visit_expr_or(node)

    def visit_import(self, node: Node.StateImport) -> None:
        pass

    def visit_def_var(self, node: Node.DefVar) -> None:
        self.table[node.name] = self.visit(node.value)

    def visit_assign(self, node: Node.NodeAssign) -> Object:
        self.table[node.left] = self.visit(node.right)
        return self.table[node.left]

    def visit_if(self, node: Node.StateIf) -> None:
        if self.visit(node.cond):
            self.visit(node.true_block)
        else:
            self.visit(node.false_block)

    def visit_while(self, node: Node.StateWhile) -> None:
        while self.visit(node.cond):
            self.visit(node.block)

    def visit_for(self, node: Node.StateFor) -> None:
        self.visit(node.init)
        while self.visit(node.check):
            self.visit(node.block)
            self.visit(node.add)

    def visit_expr_or(self, node: Node.ExprOr):
        if len(node.ands) == 1:
            return self.visit_expr_and(node.ands[0])
        else:
            res = self.visit_expr_and(node.ands[0])
            new_value = deepcopy(res)
            for i in range(1, len(node.ands)):
                new_value.value = res.attrs['_or'].trailer_call(new_value,
                                                                self.visit_expr_and(node.ands[i]))
            return new_value

    def visit_expr_and(self, node: Node.ExprAnd):
        if len(node.xors) == 1:
            return self.visit_expr_xor(node.xors[0])
        else:
            res = self.visit_expr_xor(node.xors[0])
            new_value = deepcopy(res)
            for i in range(1, len(node.xors)):
                new_value.value = res.attrs['_and'].trailer_call(new_value,
                                                                 self.visit_expr_xor(node.xors[i]))
            return new_value

    def visit_expr_xor(self, node: Node.ExprXor):
        if len(node.shifts) == 1:
            return self.visit_expr_shift(node.shifts[0])

    def visit_expr_shift(self, node: Node.ExprShift):
        if len(node.cmds) == 1:
            return self.visit_expr_cmd(node.cmds[0][1])

    def visit_expr_cmd(self, node: Node.ExprCmd):
        if len(node.lists) == 1:
            return self.visit_expr_list(node.lists[0][1])

    def visit_expr_list(self, node: Node.ExprList):
        if len(node.pipes) == 1:
            return self.visit_expr_pipe(node.pipes[0])

    def visit_expr_pipe(self, node: Node.ExprPipe):
        if len(node.ariths) == 1:
            return self.visit_expr_arith(node.ariths[0])

    def visit_expr_arith(self, node: Node.ExprArith):
        if len(node.terms) == 1:
            return self.visit_term(node.terms[0][1])
        else:
            res = self.visit_term(node.terms[0][1])
            new_val = deepcopy(res)
            for op, term in node.terms[1:]:
                new_val.value = res.attrs[{'+': '_add',
                                           '-': '_sub'}[op]].trailer_call(new_val,
                                                                          self.visit_term(term))
            return new_val

    def visit_term(self, node: Node.Term):
        if len(node.factors) == 1:
            return self.visit_factor(node.factors[0][1])
        else:
            res = self.visit_factor(node.factors[0][1])
            new_val = deepcopy(res)
            for op, fact in node.factors[1:]:
                new_val.value = res.attrs[{'*': '_mul',
                                           '/': '_div',
                                           '%': '_mod'}[op]].trailer_call(new_val,
                                                                          self.visit_factor(fact))
            return new_val

    def visit_factor(self, node: Node.Factor):
        if len(node.factors) == 0:
            return self.visit_power(node.power)
        else:
            mul = 1
            for f in node.factors:
                if f == '-':
                    mul *= -1
            res = self.visit_power(node.power)
            val = res.attrs['_mul'].trailer_call(res, Literal(BUILT_IN_INT, mul))
            return Literal(res.type, val)

    def visit_power(self, node: Node.Power):
        if len(node.atoms) == 1:
            return self.visit_expr_atom(node.atoms[0])
        else:
            res = self.visit_expr_atom(node.atoms[0])
            new_val = deepcopy(res)
            for at in node.atoms[1:]:
                new_val.value = res.attrs['_pow'].trailer_call(res,
                                                               self.visit_expr_atom(at))
            return new_val

    def visit_expr_atom(self, node: Node.ExprAtom) -> Object:
        if len(node.trailers) == 0:
            return self.visit_atom(node.atom)
        else:
            res = self.visit_atom(node.atom)
            new_value = deepcopy(res)
            for t in node.trailers:
                if isinstance(t, Node.TrailerDot) and isinstance(res, Type):
                    new_value = new_value.attrs[t.ide]
                    continue
                if isinstance(t, Node.TrailerCall):
                    new_value.value = new_value.trailer_call(*[self.visit_expr_or(e) for e in t.exprs])
                elif isinstance(t, Node.TrailerIndex):
                    new_value.value = new_value.trailer_index(*[self.visit_expr_or(e) for e in t.exprs])
                elif isinstance(t, Node.TrailerDot):
                    new_value = new_value.trailer_dot(t.ide)
            return new_value

    def visit_atom(self, node: Node.Atom) -> Object:
        if isinstance(node, Node.AtomLiteral):
            if node.type == TokenType.INTEGER:
                return Literal(BUILT_IN_INT, int(node.val))
            if node.type == TokenType.STRING:
                return Literal(BUILT_IN_STRING, str(node.val))
            if node.type == TokenType.IDENTIFIER:
                return self.table[node.val]
            if node.type == TokenType.TRUE:
                return Literal(BUILT_IN_BOOL, True)
            if node.type == TokenType.FALSE:
                return Literal(BUILT_IN_BOOL, False)
            if node.type == TokenType.NOTHING:
                raise NotImplementedError
        elif isinstance(node, Node.LiteralTuple):
            if len(node.elems) == 1:
                return self.visit_expr_or(node.elems[0])
            return Literal(BUILT_IN_TUPLE,
                           tuple([self.visit_expr_or(e).value for e in node.elems if not isinstance(e, Node.EmptyLiteral)]))
        elif isinstance(node, Node.LiteralList):
            return Literal(BUILT_IN_LIST, [self.visit_expr_or(e).value for e in node.elems])

BUILT_IN_CLASS = Type('class', dict())
BUILT_IN_FUNC = Type('function', dict())
BUILT_IN_OBJECT = Type('object', {
    'to_str': Variable('to_str', BUILT_IN_FUNC, lambda a: str(a)),
})
BUILT_IN_INT = Type('int', {
    '_add': Variable('_add', BUILT_IN_FUNC, lambda a, b: a.value+b.value),
    '_sub': Variable('_sub', BUILT_IN_FUNC, lambda a, b: a.value-b.value),
    '_mul': Variable('_mul', BUILT_IN_FUNC, lambda a, b: a.value*b.value),
    '_div': Variable('_div', BUILT_IN_FUNC, lambda a, b: a.value/b.value),
    '_mod': Variable('_mod', BUILT_IN_FUNC, lambda a, b: a.value%b.value),
    '_pow': Variable('_pow', BUILT_IN_FUNC, lambda a, b: a.value**b.value)
}, BUILT_IN_OBJECT)
BUILT_IN_STRING = Type('string', {
    '_add': Variable('_add', BUILT_IN_FUNC, lambda a, b: a.value+b.value)
}, BUILT_IN_OBJECT)
BUILT_IN_BOOL = Type('bool', {
    '_or': Variable('_or', BUILT_IN_FUNC, lambda a, b: a.value or b.value)
}, BUILT_IN_OBJECT)
BUILT_IN_TUPLE = Type('tuple', {
    'get': Variable('get', BUILT_IN_FUNC, lambda a, b: a.value[b.value])  # TODO: get 함수 구현
}, BUILT_IN_OBJECT)
BUILT_IN_LIST = Type('list', {
    'get': Variable('get', BUILT_IN_FUNC, lambda a, b: a.value[b.value])  # TODO: get 함수 구현
}, BUILT_IN_OBJECT)

GLOBAL_VARIABLES = [
    Type('system', {
        'print': Variable('print', BUILT_IN_FUNC, lambda a: print(a.value))
    }, BUILT_IN_OBJECT)
]


def execute(code):
    from parse.builder import parse
    m = SimpleMachine(GLOBAL_VARIABLES)
    m.execute(parse(code))
    return m


def main(code):
    execute(code)

if __name__ == '__main__':
    c = '''
    system.print("str".to_str());
    '''
    main(c)
