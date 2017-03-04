from tok import Token, TokenType


def parse(code: str):
    index = 0
    while index < len(code) - 1:
        tok, index = parse_token(code, index=index)
        if tok.type != TokenType.NONE:
            yield tok


def parse_token(code: str, index=0) -> (Token, int):
    current = code[index:]
    if current[0] in '\r\n\t':
        return Token(current[0], TokenType.NONE)
    if current[0] is '"':
        return parse_string(current)
    if str.isdigit(current[0]):
        return parse_number(current)


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


def parse_string(code: str) -> Token:
    res = ''
    i = 1
    while i < len(code) and code[i] != '"':
        if code[i] == '\\':
            decoded = decode_escape(code[i+1])
            if decoded is None:
                return Token(None, TokenType.ERROR)
            res += decoded
            i += 1
        else:
            res += code[i]
        i += 1
    return Token(res, TokenType.STRING)


def parse_number(code: str) -> Token:
    i = 0
    result_type = TokenType.INTEGER
    while i < len(code):
        if code[i] == '.':
            if result_type == TokenType.REAL:
                return Token(None, TokenType.ERROR)
            result_type = TokenType.REAL
        if not str.isdigit(code[i]):
            return Token(code[:i+1], result_type)
        i += 1


if __name__ == '__main__':
    print(parse_string(open('code.txt', encoding='utf-8').read()).code)
