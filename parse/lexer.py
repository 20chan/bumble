from parse.tok import Token, TokenType


def decode_escape(char: str) -> str:
    return {
        '\\': '\\',
        'n': '\n',
        't': '\t',
        'r': '\r',
        '\'': '\'',
        '"':  '"',
        '0': '\0'
    }[char]


def tokenize(code: str):
    index = 0
    while index < len(code):
        tok, _index = parse_token(code, index=index)
        index += _index
        if tok.type != TokenType.NONE:
            yield tok
    yield Token('', TokenType.EOF)


def parse_token(code: str, index=0) -> (Token, int):
    current = code[index:]
    cur = current[0]

    if cur == '/':
        return parse_comment(current)
    if cur in ' \r\n\t':
        return Token(cur, TokenType.NONE), 1
    if cur == '"':
        return parse_string(current)
    if cur == "'":
        return parse_char(current)
    if str.isdigit(cur):
        return parse_number(current)
    if cur in ['true', 'false']:
        return parse_bool(current)
    if cur in '()=,':
        return parse_operator(current)
    return parse_identifier(current)


def parse_comment(code: str) -> (Token, int):
    code_value = code[1]
    i = 0

    if code_value == '/':
        i = 2
        while i < len(code) and code[i] != '\n':
            i += 1

    if code_value == '*':
        i = 2
        while i < len(code) - 1 and code[i:i+2] != '*/':
            i += 1
        i += 2

    return Token('', TokenType.NONE), i


def parse_string(code: str) -> (Token, int):
    res = ''
    i = 1
    while i < len(code) and code[i] != '"':
        if code[i] == '\\':
            i += 1
            decode = decode_escape(code[i])
            if decode is None:
                return Token(None, TokenType.ERROR), i
            res += decode
        else:
            res += code[i]
        i += 1

    return Token(res, TokenType.STRING), i+1


def parse_char(code: str) -> (Token, int):
    return Token(code[1], TokenType.CHAR), 3


def parse_number(code: str) -> (Token, int):
    result_type = TokenType.INTEGER

    i = 0
    while i < len(code):
        if code[i] == '.':
            if result_type == TokenType.REAL:
                return Token(None, TokenType.ERROR), i
            result_type = TokenType.REAL
        elif not str.isdigit(code[i]):
            break
        i += 1

    return Token(code[:i], result_type), i


def parse_bool(code: str) -> (Token, int):
    if code.startswith('true'):
        return Token('true', TokenType.TRUE), 4
    else:
        return Token('false', TokenType.FALSE), 5


def parse_operator(code: str) -> (Token, int):
    if code[0] == '(':
        return Token('(', TokenType.LBRAKET), 1
    elif code[0] == ')':
        return Token(')', TokenType.RBRAKET), 1
    elif code[0] == '=':
        return Token('=', TokenType.EQUAL), 1
    else:
        return Token(',', TokenType.COMMA), 1


def parse_identifier(code: str) -> (Token, int):
    i = 0
    while i < len(code) and not Token.is_split_char(code[i]):
        i += 1

    return Token(code[:i], TokenType.IDENTIFIER), i


if __name__ == '__main__':
    c = open('code.txt', encoding='utf-8').read()
    print('original code')
    print(c)
    for t in tokenize(c):
        print(t)
