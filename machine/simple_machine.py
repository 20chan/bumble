from machine.basic_machine import BasicMachine
from parse.builder import parse


class SimpleMachine(BasicMachine):
    def __init__(self, code):
        self.tree = parse(code)

    def run(self):
        raise NotImplementedError
