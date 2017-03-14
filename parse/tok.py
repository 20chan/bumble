from enum import Enum


class Token:
    separators = '.,:;[]{}()'
    operator_unit = ':=+-*/%^&$|<>!'
    keywords = ['var', 'func', 'if', 'else', 'cond', 'then', 'match', 'while', 'for', 'in'
                'return', 'yield', 'skip', 'break', 'nothing', 'true', 'false']

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
    ELSEIF = 12
    COND = 13
    MATCH = 14
    WHILE = 15
    FOR = 16
    RETURN = 17
    YIELD = 18
    SKIP = 19
    BREAK = 20
    VAR = 21
    FUNC = 22
    CLASS = 23
    CALL = 24
    BIND = 25
    NOTHING = 26
    THEN = 27
    IN = 28
