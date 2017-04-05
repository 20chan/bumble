from machine.machine import Machine
from parse.tok import TokenType
from parse.AST import Node
from typing import Dict


class Type:
    types = []

    def __init__(self, name: str, attrs: Dict[str, Variable], parent=None):
        self.name = name
        self.attrs = parent.attrs
        for key in attrs.keys():
            self.attrs[key] = attrs[key]
        self.parent = parent
        Type.types += self


class Object:
    def __init__(self, typ: Type, value):
        self.type = typ
        self.value = value
        self.attrs: Dict[str, Variable] = typ.attrs

    def trailer_call(self, *args):
        return self.value(*args)

    def trailer_index(self, args):
        return self.attrs['get'].trailer_call(args)

    def trailer_dot(self, name):
        return self.attrs[name]


class Variable(Object):
    def __init__(self, name: str, typ: Type, value):
        self.name = name
        Object.__init__(self, typ, value)


class Literal(Object):
    def __init__(self, typ: Type, value):
        Object.__init__(self, typ, value)


class SimpleMachine(Machine):
    def __init__(self):
        self.table = {}

    def execute(self, node: Node.Statement):
        for s in node.sentences:
            self.visit(s)
        pass

    def visit(self, node: Node.Node):
        if isinstance(node, Node.StateImport):
            return self.visit_import(node)
        if isinstance(node, Node.ExprOr):
            return self.visit_expr_or(node)

    def visit_import(self, node: Node.StateImport) -> None:
        pass

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
            for i in range(1, len(node.ands)):
                res = res.attrs['_or'].trailer_call(self.visit_expr_and(node.ands[i]))
            return res

    def visit_expr_and(self, node: Node.ExprAnd):
        if len(node.xors) == 1:
            return self.visit_expr_xor(node.xors[0])
        else:
            res = self.visit_expr_xor(node.xors[0])
            for i in range(1, len(node.xors)):
                res = res.attrs['_and'].trailer_call(self.visit_expr_xor(node.xors[i]))
            return res

    def visit_expr_xor(self, node: Node.ExprXor):
        if len(node.shifts) == 1:
            return self.visit_expr_shift(node.shifts[0])

    def visit_expr_shift(self, node: Node.ExprShift):
        if len(node.cmds) == 1:
            return self.visit_expr_cmd(node.cmds[0])

    def visit_expr_cmd(self, node: Node.ExprCmd):
        if len(node.lists) == 1:
            return self.visit_expr_list(node.lists[0])

    def visit_expr_list(self, node: Node.ExprList):
        if len(node.pipes) == 1:
            return self.visit_expr_pipe(node.pipes[0])

    def visit_expr_pipe(self, node: Node.ExprPipe):
        if len(node.ariths) == 1:
            return self.visit_expr_arith(node.ariths[0])

    def visit_expr_arith(self, node: Node.ExprArith):
        if len(node.terms) == 1:
            return self.visit_term(node.terms[0])

    def visit_term(self, node: Node.Term):
        if len(node.factors) == 1:
            return self.visit_factor(node.factors[0])

    def visit_factor(self, node: Node.Factor):
        if len(node.factors) == 0:
            return self.visit_power(node.power)

    def visit_power(self, node: Node.Power):
        if len(node.atoms) == 1:
            return self.visit_expr_atom(node.atoms[0])

    def visit_expr_atom(self, node: Node.ExprAtom):
        if len(node.trailers) == 0:
            return self.visit_atom(node.atom)
        else:
            res = self.visit_atom(node.atom)
            for t in node.trailers:
                if isinstance(t, Node.TrailerCall):
                    res = res.trailer_call(*[self.visit_expr_or(e) for e in t.exprs])
                elif isinstance(t, Node.TrailerIndex):
                    res = res.trailer_index(*[self.visit_expr_or(e) for e in t.exprs])
                elif isinstance(t, Node.TrailerDot):
                    res = res.trailer_dot(t.ide)

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
            return Literal(BUILT_IN_TUPLE, tuple([self.visit_expr_or(e) for e in node.elems]))
        elif isinstance(node, Node.LiteralList):
            return Literal(BUILT_IN_LIST, [self.visit_expr_or(e) for e in node.elems])

BUILT_IN_CLASS = Type('class', dict())
BUILT_IN_FUNC = Type('function', dict())
BUILT_IN_OBJECT = Type('object', {
    'to_str': Variable('to_str', BUILT_IN_FUNC, lambda a: str(a)),
})
BUILT_IN_INT = Type('int', {
    '_add': Variable('_add', BUILT_IN_FUNC, lambda a, b: a+b),
    '_sub': Variable('_sub', BUILT_IN_FUNC, lambda a, b: a-b),
    '_mul': Variable('_mul', BUILT_IN_FUNC, lambda a, b: a*b),
    '_div': Variable('_div', BUILT_IN_FUNC, lambda a, b: a/b),
    '_mod': Variable('_mod', BUILT_IN_FUNC, lambda a, b: a%b)
}, BUILT_IN_OBJECT)
BUILT_IN_STRING = Type('string', {
    'operator+': Variable('operator+', BUILT_IN_FUNC, lambda a, b: a+b)
})
BUILT_IN_BOOL = Type('bool', {
    '_or': Variable('_or', BUILT_IN_FUNC, lambda a, b: a or b)
})
BUILT_IN_TUPLE = Type('tuple', {
    'get': Variable('get', BUILT_IN_FUNC, None)  # TODO: get 함수 구현
})
BUILT_IN_LIST = Type('list', {
    'get': Variable('get', BUILT_IN_FUNC, None)  # TODO: get 함수 구현
})
