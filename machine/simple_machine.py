from machine.basic_machine import Machine
from parse.tok import TokenType
from parse.AST import Node
from typing import List, Dict


class Symbol:
    def __init__(self, name, typ=None, value=None):
        self.name = name
        self.type = typ
        self.value = value


class VarSymbol(Symbol):
    def __init__(self, name, typ, value=None):
        Symbol.__init__(self, name, typ, value)


class LiteralSymbol(Symbol):
    def __init__(self, typ, value):
        Symbol.__init__(self, None, typ, value)


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        Symbol.__init__(self, name)


class SymbolTable:
    def __init__(self):
        from collections import OrderedDict
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        types = ['INTEGER', 'REAL', 'STRING', 'BOOL']
        for typ in types:
            self.define(BuiltinTypeSymbol(typ))

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def __getitem__(self, name) -> Symbol:
        return self._symbols[name]


class SimpleMachine(Machine):
    def __init__(self):
        self.table = SymbolTable()

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
