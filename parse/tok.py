from enum import Enum


class Token:
    separators = '.,:;[]{}()'
    operator_unit = '=+-*/%^&$<>!'
    keywords = ['var', 'func', 'if', 'match', 'while', 'return', 'yield', 'skip', 'break']

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
    IDENTIFIER = 7
    _IF = 8
    _MATCH = 9
    _WHILE = 10
    _RETURN = 11
    _YIELD = 12
    _SKIP = 13
    _BREAK = 14
    _DECLARE_VAR = 15
    _DECLARE_FUNC = 16
    _ASSIGN = 17
    _CALL = 18
