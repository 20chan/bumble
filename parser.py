from tok import Token, TokenType


def parse(code: str):
    index = 0
    while index < len(code) - 1:
        tok, index = parse_token(code, index=index)
        if tok.type != TokenType.NONE:
            yield tok


def parse_token(code, index=0) -> (Token, int):
    current = code[index:]
    if current[0] in '\r\n\t':
        return Token(current[0], TokenType.NONE)
    if current[0] is '"':
        return parse_string(current)


def decode_escape(char):
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


def parse_string(code):
    res = ''
    i = 1
    while i < len(code) and code[i] != '"':
        if code[i] == '\\':
            res += decode_escape(code[i+1])
            i += 1
        else:
            res += code[i]
        i += 1
    return res

print(parse_string('"wow \\tthis is \\nawesome" lol'))
