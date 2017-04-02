from enum import Enum


class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

precedences = {
    '=': (1, Direction.RIGHT),
    ':=': (1, Direction.RIGHT),
    '|>': (2, Direction.LEFT),
    '=>': (3, Direction.RIGHT),  # => 요것도 연산자 우선순위를 따지나?
    '.': (2, Direction.LEFT),
    '()': (2, Direction.LEFT),
    '||': (3, Direction.LEFT),
    '&&': (4, Direction.RIGHT),
    '^': (5, Direction.LEFT),
    '<<': (6, Direction.LEFT),
    '>>': (6, Direction.LEFT),
    '<': (7, Direction.LEFT),
    '<=': (7, Direction.LEFT),
    '>': (7, Direction.LEFT),
    '>=': (7, Direction.LEFT),
    '==': (7, Direction.LEFT),
    '!=': (7, Direction.LEFT),
    ':': (8, Direction.RIGHT),
    '++': (8, Direction.RIGHT),
    '+': (9, Direction.LEFT),
    '-': (9, Direction.LEFT),
    '*': (10, Direction.LEFT),
    '/': (10, Direction.LEFT),
    '%': (10, Direction.LEFT),
    '**': (11, Direction.RIGHT)
}


