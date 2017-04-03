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

    def simplify(self):
        if len(self.sentences) == 1:
            return self.sentences[0].simplify()
        else:
            return [s.simplify() for s in self.sentences]


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

    def simplify(self):
        return ['for', self.init.simplify(), self.check.simplify(), self.add.simplify(),
                self.add.simplify(), self.block.simplify()]


class StateCond(Sentence):
    def __init__(self, cond, states, otherwise=None):
        self.cond = cond
        self.states = states
        self.otherwise = otherwise

    def simplify(self):
        otherwise = ["otherwise", self.otherwise.simplify()] if self.otherwise is not None else []
        return ["cond", self.cond.simplify(), *[s.simplify() for s in self.states]] + otherwise


class StateMatch(Sentence):
    def __init__(self, cond, states):
        self.cond = cond
        self.states = states


class StateTry(Sentence):
    def __init__(self, try_, catch_, finally_):
        self.try_ = try_
        self.catch_ = catch_
        self.finally_ = finally_

    def simplify(self):
        catch = ["catch", self.catch_.simplify()] if self.catch_ is not None else []
        final = ["finally", self.finally_.simplify()] if self.finally_ is not None else []
        return ["try", self.try_.simplify()] + catch + final


class StateEnum(Sentence):
    def __init__(self, name, maps):
        self.name = name
        self.maps = maps

    def simplify(self):
        return ["enum", self.name, "{", *self.maps, "}"]


class DefClass(Sentence):
    def __init__(self, name, parent, sentences):
        self.name = name
        self.parent = parent
        self.sentences = sentences

    def simplify(self):
        if self.parent is None:
            return ["class", self.name, self.sentences.simplify()]
        else:
            return ["class", self.name, ":", self.parent, self.sentences.simplify()]


class DefFunc(Sentence):
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block

    def simplify(self):
        return ["func", self.name, "(", *self.args, ")", self.block.simplify()]


class DefVar(Sentence):
    def __init__(self, name, val=None):
        self.name = name
        self.value = val

    def simplify(self):
        if self.value is None:
            return ["var", self.name]
        else:
            return ["var", self.name, "=", self.value.simplify()]


class DefLambda(Expression):
    def __init__(self, exprs, block):
        self.exprs = exprs
        self.block = block


class NodeAssign(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return [self.left.simplify(), "=", self.right.simplify()]


class NodeBind(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def simplify(self):
        return [self.left.simplify(), ":=", self.right.simplify()]


class NodeCall(Expression):
    def __init__(self, expr):
        self.expr = expr


class ExprWildcard(Expression):
    def __init__(self):
        pass

    def simplify(self):
        return '_'


class ExprOr(Expression):
    def __init__(self, ands: List):
        self.ands = ands

    def simplify(self):
        if len(self.ands) == 1:
            return self.ands[0].simplify()
        else:
            return [s.simplify() for s in self.ands]


class ExprAnd(Expression):
    def __init__(self, xors: List):
        self.xors = xors

    def simplify(self):
        if len(self.xors) == 1:
            return self.xors[0].simplify()
        else:
            return [s.simplify() for s in self.xors]


class ExprXor(Expression):
    def __init__(self, shifts: List):
        self.shifts = shifts

    def simplify(self):
        if len(self.shifts) == 1:
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
        if len(self.cmds) == 1:
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
        if len(self.lists) == 1:
            return self.lists[0][1].simplify()
        else:
            res = [self.lists[0][1].simplify()]
            for l in self.lists[1:]:
                res.append(l[0])
                res.append(l[1].simplify())


class ExprList(Expression):
    def __init__(self, pipes):
        self.pipes = pipes

    def simplify(self):
        if len(self.pipes) == 1:
            return self.pipes[0][1].simplify()
        else:
            res = [self.pipes[0][1].simplify()]
            for l in self.pipes[1:]:
                res.append(l[0])
                res.append(l[1].simplify())


class ExprPipe(Expression):
    def __init__(self, ariths):
        self.ariths = ariths

    def simplify(self):
        if len(self.ariths) == 1:
            return self.ariths[0].simplify()
        else:
            return [s.simplify() for s in self.ariths]


class ExprArith(Expression):
    def __init__(self, terms):
        self.terms = terms

    def simplify(self):
        if len(self.terms) == 1:
            return self.terms[0][1].simplify()
        else:
            res = [self.terms[0][1].simplify()]
            for l in self.terms[1:]:
                res.append(l[0])
                res.append(l[1].simplify())
            return res


class Term(Expression):
    def __init__(self, factors):
        self.factors = factors

    def simplify(self):
        if len(self.factors) == 1:
            return self.factors[0][1].simplify()
        else:
            res = [self.factors[0][1].simplify()]
            for l in self.factors[1:]:
                res.append(l[0])
                res.append(l[1].simplify())


class Factor(Expression):
    def __init__(self, factors: List[str], power):
        """
        factor := (+,-)* <power>
        :param factors: 형식은 [("+"| "-")*]
        :param power: <power>
        """
        self.factors = factors
        self.power = power

    def simplify(self):
        if len(self.factors) == 0:
            return self.power.simplify()
        else:
            return self.factors + [self.power.simplify()]


class Power(Expression):
    def __init__(self, atoms):
        self.atoms = atoms

    def simplify(self):
        if len(self.atoms) == 1:
            return self.atoms[0].simplify()
        else:
            return [s.simplify for s in self.atoms]


class ExprAtom(Expression):
    def __init__(self, atom, trailers):
        self.atom = atom
        self.trailers = trailers

    def simplify(self):
        if len(self.trailers) == 0:
            return self.atom.simplify()
        else:
            return [self.atom.simplify()] + [s.simplify() for s in self.trailers]


class Atom(Expression):
    def __init__(self, code):
        self.code = code

    def simplify(self):
        return self.code


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

    def simplify(self):
        if len(self.exprs) == 0:
            return self.exprs[0].simplify()
        else:
            return [s.simplify() for s in self.exprs]


class TrailerIndex(Trailer):
    def __init__(self, exprs):
        self.exprs = exprs

    def simplify(self):
        if len(self.exprs) == 0:
            return self.exprs[0].simplify()
        else:
            return ["["] + [s.simplify() for s in self.exprs] + ["]"]


class TrailerDot(Trailer):
    def __init__(self, ide):
        self.ide = ide

    def simplify(self):
        return [".", self.ide]

