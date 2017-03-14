from enum import Enum


class Token:
    separators = '.,:;[]{}()'
    operator_unit = '=+-*/%^&$|<>!'
    keywords = ['var', 'func', 'if', 'else', 'cond', 'then', 'match', 'while',
                'return', 'yield', 'skip', 'break', 'none', 'true', 'false']

    def __init__(self, code, tok_type):
        self.code = code
        self.type = tok_type

    def __repr__(self):
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
    TRUE = 5
    FALSE = 6
    SEPARATOR = 7
    OPERATOR = 8
    IDENTIFIER = 9
    IF = 10
    ELSE = 11
    MATCH = 12
    WHILE = 13
    RETURN = 14
    YIELD = 15
    SKIP = 16
    BREAK = 17
    DECLARE_VAR = 18
    DECLARE_FUNC = 19
    ASSIGN = 20
    CALL = 21
