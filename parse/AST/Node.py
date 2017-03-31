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


class NodeLiteral(Expression):
    def __init__(self, val):
        self.val = val


class NodeInteger(NodeLiteral):
    def __init__(self, val):
        NodeLiteral.__init__(self, val)


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
