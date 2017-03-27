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
    def __init__(self, cond, loop):
        self.cond = cond
        self.loop = loop


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
