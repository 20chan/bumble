from typing import List, Tuple


class Node:
    def __repr__(self):
        return '<{}>'.format(type(self).__name__)

    def simplify(self):
        pass


class Statement(Node):
    def __init__(self, sentences):
        if isinstance(sentences, Sentence):
            self.sentences = [sentences]
        else:
            self.sentences = sentences


class Sentence(Node):
    pass


class Expression(Sentence):
    pass


class StateIf(Sentence):
    def __init__(self, cond: Expression, true_block: Statement, false_block: Statement):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

    def simplify(self):
        if self.false_block is None:
            return ['if', self.cond.simplify(), self.true_block.simplify(),
                    'else', self.false_block.simplify()]
        else:
            return ['if', self.cond.simplify(), self.true_block.simplify()]


class StateWhile(Sentence):
    def __init__(self, cond: Expression, block: Statement):
        self.cond = cond
        self.block = block

    def simplify(self):
        return ['while', self.cond.simplify(), self.block.simplify()]


class StateFor(Sentence):
    def __init__(self, init, check, add, block):
        self.init = init
        self.check = check
        self.add = add
        self.block = block


class StateCond(Sentence):
    def __init__(self, cond, states, otherwise=None):
        self.cond = cond
        self.states = states
        self.otherwise = otherwise


class StateMatch(Sentence):
    def __init__(self, cond, states):
        self.cond = cond
        self.states = states


class StateTry(Sentence):
    def __init__(self, try_, catch_, finally_):
        self.try_ = try_
        self.catch_ = catch_
        self.finally_ = finally_


class StateEnum(Sentence):
    def __init__(self, name, keys, values):
        self.name = name
        self.keys = keys
        self.values = values


class DefClass(Sentence):
    def __init__(self, name, parent, sentences):
        self.name = name
        self.parent = parent
        self.sentences = sentences


class DefFunc(Sentence):
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block


class DefVar(Sentence):
    def __init__(self, name, val=None):
        self.name = name
        self.value = val


class DefLambda(Expression):
    def __init__(self, exprs, block):
        self.exprs = exprs
        self.block = block


class NodeAssign(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class NodeBind(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class NodeCall(Expression):
    def __init__(self, expr):
        self.expr = expr


class ExprWildcard(Expression):
    def __init__(self):
        pass

    def simplify(self):
        return '_'


class ExprOr(Expression):
    def __init__(self, ands: List[ExprAnd]):
        self.ands = ands

    def simplify(self):
        if len(self.ands) == 0:
            return self.ands[0].simplify()
        else:
            return [s.simplify() for s in self.ands]


class ExprAnd(Expression):
    def __init__(self, xors: List[ExprXor]):
        self.xors = xors

    def simplify(self):
        if len(self.xors) == 0:
            return self.xors[0].simplify()
        else:
            return [s.simplify() for s in self.xors]


class ExprXor(Expression):
    def __init__(self, shifts: List[ExprShift]):
        self.shifts = shifts

    def simplify(self):
        if len(self.shifts) == 0:
            return self.shifts[0].simplify()
        else:
            return [s.simplify() for s in self.shifts]


class ExprShift(Expression):
    def __init__(self, cmds: List[Tuple]):
        """
        a >> b << c 의 코드는 다음과 같이 파싱된다
        :param cmds: [(None, a), (">>", b), ("<<", c)]
        """
        self.cmds = cmds

    def simplify(self):
        if len(self.cmds) == 0:
            return self.cmds[0][1].simplify()
        else:
            res = [self.cmds[0][1].simplify()]
            for c in self.cmds[1:]:
                res.append(c[0])
                res.append(c[1].simplify())


class ExprCmd(Expression):
    def __init__(self, lists):
        """
        a > b != c 의 코드는 다음과 같이 파싱된다
        :param lists: [(None, a), (">", b), ("!=", c)]
        """
        self.lists = lists

    def simplify(self):
        if len(self.lists) == 0:
            return self.lists[0][1].simplify()
        else:
            res = [self.lists[0][1].simplify()]
            for l in self.lists[1:]:
                res.append(l[0])
                res.append(l[1].simplify())


class ExprList(Expression):
    def __init__(self, pipe, pipes):
        self.pipe = pipe
        self.pipes = pipes


class ExprPipe(Expression):
    def __init__(self, arith, ariths):
        self.arith = arith
        self.ariths = ariths


class ExprArith(Expression):
    def __init__(self, term, terms):
        self.term = term
        self.terms = terms


class Term(Expression):
    def __init__(self, factor, factors):
        self.factor = factor
        self.factors = factors


class Factor(Expression):
    def __init__(self, factors, power):
        """
        factor := (+,-)* <power>
        :param factors: 형식은 [("+"| "-")*]
        :param power: <power>
        """
        self.factors = factors
        self.power = power


class Power(Expression):
    def __init__(self, atoms):
        self.atoms = atoms


class ExprAtom(Expression):
    def __init__(self, atom, trailers):
        self.atom = atom
        self.trailers = trailers


class Atom(Expression):
    pass


class NodeLiteral(Expression):
    def __init__(self, val):
        self.val = val


class NodeInteger(NodeLiteral):
    def __init__(self, val):
        NodeLiteral.__init__(self, val)


class Trailer(Node):
    pass


class TrailerCall(Trailer):
    def __init__(self, exprs):
        self.exprs = exprs


class TrailerIndex(Trailer):
    def __init__(self, exprs):
        self.exprs = exprs


class TrailerDot(Trailer):
    def __init__(self, ide):
        self.ide = ide
