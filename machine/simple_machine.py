from machine.basic_machine import Machine
from parse.tok import TokenType
from parse.AST import Node
from typing import List, Dict


class Class:
    def __init__(self, parent, sentences: List[Node.Sentence]):
        self.parent = parent
        self.sentences = sentences

    def make_instance(self) -> Object:
        pass


class Object:
    pass


class SimpleMachine(Machine):
    pass
