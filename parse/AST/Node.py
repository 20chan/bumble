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
    def __init__(self, init, check, add, loop):
        self.init = init
        self.check = check
        self.add = add
        self.loop = loop


class LambdaDef(Expression):
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
    def __init__(self, ide, exp=None):
        self.id = ide
        self.exp = exp


class NodeBind(Expression):
    def __init__(self, ide, exp):
        self.ide = ide
        self.exp = exp


class NodeCall(Expression):
    def __init__(self, exp, *args):
        self.exp = exp
        self.args = args
