class Node:
    def __repr__(self):
        return '<{}>'.format(type(self).__name__)


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
    def __init__(self, cond, true_block, false_block):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block


class StateWhile(Sentence):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


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


class ExprOr(Expression):
    def __init__(self, ands):
        self.ands = ands


class ExprAnd(Expression):
    def __init__(self, xors):
        self.xors = xors


class ExprXor(Expression):
    def __init__(self, shifts):
        self.shifts = shifts


class ExprShift(Expression):
    def __init__(self, cmd, cmds):
        """
        a >> b << c 의 코드는 다음과 같이 파싱된다
        :param cmd: a
        :param cmds: [(">>", b), ("<<", c)]
        """
        self.cmd = cmd
        self.cmds = cmds


class ExprCmd(Expression):
    def __init__(self, l, ls):
        """
        a > b != c 의 코드는 다음과 같이 파싱된다
        :param l: a
        :param ls: (">", b), ("!=", c)
        """
        self.l = l
        self.ls = ls


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
