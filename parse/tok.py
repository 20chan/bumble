from enum import Enum


class Token:

    def __init__(self, code, tok_type):
        self.code = code
        self.type = tok_type

    def __repr__(self):
        return 'Type : {}, Code : {}'\
            .format(str(self.type).split('.')[1], self.code)

    @staticmethod
    def is_split_char(char):
        return char in ' \r\n\t()='

    def is_literal(self):
        return self.type in\
               [TokenType.INTEGER, TokenType.REAL, TokenType.STRING, TokenType.CHAR, TokenType.TRUE, TokenType.FALSE]


class TokenType(Enum):
    ERROR = -1
    NONE = 0
    EOF = 1
    INTEGER = 2
    REAL = 3
    STRING = 4
    CHAR = 5
    TRUE = 6
    FALSE = 7
    IDENTIFIER = 8
    WILDCARD = 9
    LBRAKET = 10
    RBRAKET = 11
    EQUAL = 12
    COMMA = 13
