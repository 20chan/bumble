from machine.basic_machine import Machine
from parse.tok import TokenType
from parse.AST import Node
from typing import List, Dict


class Symbol:
    def __init__(self, name, typ=None):
        self.name = name
        self.type = typ


class VarSymbol(Symbol):
    def __init__(self, name, typ):
        Symbol.__init__(self, name, typ)


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


class SimpleMachine(Machine):
    pass
