from parse.tok import Token, TokenType


def decode_escape(char: str) -> str:
    if char == '\\':
        return '\\'
    if char == 'n':
        return '\n'
    if char == 't':
        return '\t'
    if char == 'r':
        return '\r'
    if char == '\'':
        return '\''
    if char == '"':
        return '"'
    if char == '0':
        return '\0'

    return None


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
    if current[0] in ' \r\n\t':
        return Token(current[0], TokenType.NONE), 1
    if current[0] is '"':
        return parse_string(current)
    if str.isdigit(current[0]):
        return parse_number(current)
    if current[0] in Token.operator_unit:
        return parse_operator(current)
    if current[0] in Token.separators:
        return parse_separator(current)
    return parse_identifier(current)


def parse_string(code: str) -> (Token, int):
    res = ''
    i = 1
    while i < len(code) and code[i] != '"':
        if code[i] == '\\':
            decoded = decode_escape(code[i+1])
            i += 1  # 디코드하면 한글자 사라지므로 실제 인덱스는 1증가
            if decoded is None:
                return Token(None, TokenType.ERROR), i
            res += decoded
        else:
            res += code[i]
        i += 1
    return Token(res, TokenType.STRING), i+1


def parse_number(code: str) -> (Token, int):
    i = 0
    result_type = TokenType.INTEGER
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
    if code[:i] in Token.keywords:
        return Token(code[:i], TokenType.KEYWORD), i
    else:
        return Token(code[:i], TokenType.IDENTIFIER), i


if __name__ == '__main__':
    c = open('code.txt', encoding='utf-8').read()
    print('original code')
    print(c)
    for t in tokenize(c):
        print(t)
