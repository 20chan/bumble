from enum import Enum


class Token:
    separators = '.,:;[]{}()'
    operator_unit = '=+-*/%^&$<>!'
    keywords = ['def', 'return']

    def __init__(self, code, tok_type):
        self.code = code
        self.type = tok_type

    def __str__(self):
        return 'Type : {}, Code : {}'\
            .format(str(self.type).split('.')[1], self.code)

    @staticmethod
    def is_split_char(char):
        return char in Token.separators or \
            char in Token.operator_unit or \
            char in ' \r\n\t'


class TokenType(Enum):
    ERROR = -1
    NONE = 0
    EOF = 1
    INTEGER = 2
    REAL = 3
    STRING = 4
    SEPARATOR = 5
    OPERATOR = 6
    KEYWORD = 7
    IDENTIFIER = 8
