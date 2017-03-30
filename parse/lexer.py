from parse.tok import Token, TokenType


def decode_escape(char: str) -> str:
    switch_map = {
        '\\': '\\',
        'n': '\n',
        't': '\t',
        'r': '\r',
        '\'': '\'',
        '"':  '"',
        '0': '\0'
    }

    return switch_map.get(char)


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

    if cur is '/':
        return parse_comment(current)
    if cur in ' \r\n\t':
        return Token(cur, TokenType.NONE), 1
    if cur is '"':
        return parse_string(current)
    if str.isdigit(cur):
        return parse_number(current)
    if cur in Token.operator_unit:
        return parse_operator(current)
    if cur in Token.separators:
        return parse_separator(current)
    return parse_identifier(current)


def parse_comment(code: str) -> (Token, int):
    codeValue = code[1]

    if not codeValue in '/*':
        i = 0

    if codeValue == '/':
        i = 2
        while i < len(code) and code[i] != '\n':
            i += 1

    if codeValue == '*':
        i = 2
        while i < len(code) - 1 and code[i:i+2] != '*/':
            i += 1
        i += 2

    return Token('', TokenType.NONE), i


def parse_string(code: str) -> (Token, int):
    res = ''
    i = 1
    while i < len(code) and code[i] != '"':
        if code[i] != '\\':
            res += code[i]

        i += 1
        decode = decode_escape(code[i])
        if decode is None:
            return Token(None, TokenType.ERROR), i

        res += decode
        i += 1

    return Token(res, TokenType.STRING), i+1


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


def parse_operator(code: str) -> (Token, int):
    if code[0] == ':' and code[1] != '=':
        return parse_separator(code)

    i = 0
    while code[i] in Token.operator_unit:
        i += 1

    # code[i]가 operator가 아니므로 i+1이 아닌 i를 리턴
    return Token(code[:i], TokenType.OPERATOR), i


def parse_separator(code: str) -> (Token, int):
    return Token(code[0], TokenType.SEPARATOR), 1


def parse_identifier(code: str) -> (Token, int):
    i = 0
    while not Token.is_split_char(code[i]):
        i += 1

    if code[:i] not in Token.keywords:
        return Token(code[:i], TokenType.IDENTIFIER), i

    syntax = code[:i]
    stateToken = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'match': TokenType.MATCH,
        'cond': TokenType.COND,
        'then': TokenType.THEN,
        'in': TokenType.IN,
        'while': TokenType.WHILE,
        'return': TokenType.RETURN,
        'yield': TokenType.YIELD,
        'skip': TokenType.SKIP,
        'break': TokenType.BREAK,
        'var': TokenType.VAR,
        'func': TokenType.FUNC,
        'class': TokenType.CLASS,
        'nothing': TokenType.NOTHING,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE
    }

    return Token(syntax, stateToken[syntax]), i


if __name__ == '__main__':
    c = open('code.txt', encoding='utf-8').read()
    print('original code')
    print(c)
    for t in tokenize(c):
        print(t)
