from enum import Enum


class Token:
    def __init__(self, code, type):
        self.code = code
        self.type = type


class TokenType(Enum):
    ERROR = -1
    NONE = 0
    EOF = 1
    INTEGER = 2
    REAL = 3
    STRING = 4
    IDENTIFIER = 5
