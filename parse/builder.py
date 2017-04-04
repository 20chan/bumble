from parse.lexer import tokenize
from parse.tok import Token, TokenType
import parse.AST.Node as Node
# import better_exceptions
from typing import List


class Parser:
    def __init__(self, code: str):
        self.code = code
        self._toks = list(tokenize(code))

    def pop_tok(self):
        return self._toks.pop(0)

    @property
    def top(self) -> Token:
        return self._toks[0]

    def parse(self) -> Node.Statement:
        res = []
        while self.top.type != TokenType.EOF:
            res.append(self.parse_sentence())

        return Node.Statement(res)

    def check_pop(self, tok):
        assert(self.pop_tok().code == tok)

    def parse_sentence(self) -> Node.Sentence:
        if self.top.type == TokenType.IF:
            return self.parse_if()
        if self.top.type == TokenType.WHILE:
            return self.parse_while()
        if self.top.type == TokenType.FOR:
            return self.parse_for()
        if self.top.type == TokenType.COND:
            return self.parse_cond()
        if self.top.type == TokenType.MATCH:
            return self.parse_match()
        if self.top.type == TokenType.TRY:
            return self.parse_try()
        if self.top.type == TokenType.ENUM:
            return self.parse_enum()
        if self.top.type == TokenType.CLASS:
            return self.parse_class()
        if self.top.type == TokenType.FUNC:
            return self.parse_func()
        if self.top.type == TokenType.VAR:
            return self.parse_var()
        # if self.top.type == TokenType.IDENTIFIER:
        return self.parse_id()

    def parse_block(self) -> List[Node.Sentence]:
        res = []
        self.check_pop('{')
        while self.top.code != "}":
            res.append(self.parse_sentence())
        self.check_pop('}')
        return res

    def parse_statement(self) -> Node.Statement:
        if self.top.code == "{":
            return Node.Statement(self.parse_block())
        else:
            return Node.Statement(self.parse_sentence())

    def parse_if(self) -> Node.StateIf:
        self.check_pop('if')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        true_block = self.parse_statement()

        if self.pop_tok().TokenType == TokenType.ELSE:
            false_block = self.parse_statement()
        else:
            false_block = None

        return Node.StateIf(cond, true_block, false_block)

    def parse_while(self) -> Node.StateWhile:
        self.check_pop('while')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        block = self.parse_statement()

        return Node.StateWhile(cond, block)

    def parse_for(self) -> Node.StateFor:
        self.check_pop('for')
        self.check_pop('(')
        init = self.parse_expr()
        check = self.parse_expr()
        add = self.parse_expr()
        block = self.parse_statement()

        return Node.StateFor(init, check, add, block)

    def parse_cond(self) -> Node.StateCond:
        self.check_pop('cond')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        self.check_pop('{')
        states = []
        other = None
        while self.top.code != '}':
            pat = self.parse_expr()
            self.check_pop('then')
            stmt = self.parse_statement()
            states.append((pat, stmt))
        if self.top.code == 'otherwise':
            self.check_pop('otherwise')
            other = self.parse_expr()
        self.check_pop('}')

        return Node.StateCond(cond, states, other)

    def parse_match(self) -> Node.StateMatch:
        self.check_pop('match')
        self.check_pop('(')
        cond = self.parse_expr()
        self.check_pop(')')
        self.check_pop('{')
        states = []
        while self.top.code != '}':
            pat = self.parse_expr()
            self.check_pop('then')
            stmt = self.parse_statement()
            states.append((pat, stmt))

        self.check_pop('}')
        return Node.StateMatch(cond, states)

    def parse_try(self) -> Node.StateTry:
        self.check_pop('try')
        try_block = self.parse_block()
        catch_block = None
        finally_block = None
        if self.top.code == 'catch':
            self.check_pop('catch')
            catch_block = self.parse_block()
        if self.top.code == 'finally':
            self.check_pop('finally')
            finally_block = self.parse_block()

        return Node.StateTry(try_block, catch_block, finally_block)

    def parse_enum(self) -> Node.StateEnum:
        self.check_pop('enum')
        name = self.pop_tok()
        self.check_pop('{')
        maps = []
        while self.top.code != '}':
            ide = self.pop_tok()
            val = self.pop_tok() if self.top.code == '=' else None
            maps.append((ide, val))
        self.check_pop('}')

        return Node.StateEnum(name, maps)

    def parse_class(self) -> Node.DefClass:
        self.check_pop('class')
        name = self.pop_tok()
        parent = None
        if self.top.code == ':':
            self.check_pop(':')
            parent = self.pop_tok()
        self.check_pop('{')
        sentences = []
        while self.top != '}':
            sentences.append(self.parse_sentence())
        self.check_pop('}')

        return Node.DefClass(name, parent, sentences)

    def parse_func(self) -> Node.DefFunc:
        self.check_pop('func')
        name = self.pop_tok()
        args = self.parse_args()
        block = self.parse_block()

        return Node.DefFunc(name, args, block)

    def parse_args(self) -> List[str]:
        res = []
        self.check_pop('(')
        while self.top.code == '':
            res.append(self.pop_tok())
        self.check_pop(')')
        return res

    def parse_var(self) -> Node.DefVar:
        self.check_pop('var')
        name = self.pop_tok()
        if self.top.code == '=':
            self.check_pop('=')
            val = self.parse_expr()
        self.check_pop(';')

        return Node.DefVar(name, val)

    def parse_id(self) -> Node.Expression:
        identifier = self.parse_expr()
        if self.top.code == '=':
            return self.parse_assign(identifier)
        if self.top.type == TokenType.BIND:
            return self.parse_bind(identifier)

        return self.parse_call(identifier)

    def parse_assign(self, ide) -> Node.NodeAssign:
        left = ide
        self.check_pop('=')
        right = self.parse_expr()
        self.check_pop(';')

        return Node.NodeAssign(left, right)

    def parse_bind(self, ide) -> Node.NodeBind:
        left = ide
        self.check_pop(':=')
        right = self.parse_expr()
        self.check_pop(';')

        return Node.NodeBind(left, right)

    def parse_call(self, ide) -> Node.Expression:
        self.check_pop(';')

        return ide

    def parse_expr(self) -> Node.Expression:
        # TODO: parse lambda
        if self.top.code == '_':
            self.check_pop('_')
            return Node.ExprWildcard()
        return self.parse_or_expr()

    def parse_or_expr(self) -> Node.ExprOr:
        ands = [self.parse_and_expr()]
        while self.top.code == '||':
            self.check_pop('||')
            ands.append(self.parse_and_expr())

        return Node.ExprOr(ands)

    def parse_and_expr(self) -> Node.ExprAnd:
        xors = [self.parse_xor_expr()]
        while self.top.code == '&&':
            self.check_pop('&&')
            xors.append(self.parse_xor_expr())

        return Node.ExprAnd(xors)

    def parse_xor_expr(self) -> Node.ExprXor:
        shifts = [self.parse_shift_expr()]
        while self.top.code == '^':
            self.check_pop('^')
            shifts.append(self.parse_shift_expr())

        return Node.ExprXor(shifts)

    def parse_shift_expr(self) -> Node.ExprShift:
        cmds = [(None, self.parse_cmd_expr())]
        while self.top.code in ['>>', '<<']:
            tok = self.pop_tok().code
            cmds.append((tok, self.parse_cmd_expr()))

        return Node.ExprShift(cmds)

    def parse_cmd_expr(self) -> Node.ExprCmd:
        lists = [(None, self.parse_list_expr())]
        while self.top.code in ["<", ">", "==", "<=", ">=", "!="]:
            tok = self.pop_tok().code
            lists.append((tok, self.parse_list_expr()))

        return Node.ExprCmd(lists)

    def parse_list_expr(self) -> Node.ExprList:
        pipes = [(None, self.parse_pipe_expr())]
        while self.top.code in [":", "++"]:
            tok = self.pop_tok().code
            pipes.append((tok, self.parse_pipe_expr()))

        return Node.ExprList(pipes)

    def parse_pipe_expr(self) -> Node.ExprPipe:
        ariths = [ self.parse_arith_expr()]
        while self.top.code == '|>':
            ariths.append(self.parse_arith_expr())

        return Node.ExprPipe(ariths)

    def parse_arith_expr(self) -> Node.ExprArith:
        terms = [(None, self.parse_term())]
        while self.top.code in ['+', '-']:
            tok = self.pop_tok().code
            terms.append((tok, self.parse_term()))

        return Node.ExprArith(terms)

    def parse_term(self) -> Node.Term:
        factors = [(None, self.parse_factor())]
        while self.top.code in ['*', '/', '%']:
            tok = self.pop_tok().code
            factors.append((tok, self.parse_factor()))

        return Node.Term(factors)

    def parse_factor(self) -> Node.Factor:
        factors = []
        while self.top.code in ['+', '-']:
            factors.append(self.pop_tok().code)
        power = self.parse_power()

        return Node.Factor(factors, power)

    def parse_power(self) -> Node.Power:
        atoms = [self.parse_atom_expr()]
        while self.top.code == '**':
            self.check_pop('**')
            atoms.append(self.parse_atom_expr())

        return Node.Power(atoms)

    def parse_atom_expr(self) -> Node.ExprAtom:
        atom = self.parse_atom()
        trailers = []
        while self.top.code in ['(', '[', '.']:
            trailers.append(self.parse_trailer())

        return Node.ExprAtom(atom, trailers)

    def parse_atom(self) -> Node.Atom:
        if self.top.code == '(':
            return self.parse_tuple()
        if self.top.code == '[':
            return self.parse_list()
        if self.top.code == '{':
            return self.parse_map()

        return Node.AtomLiteral(self.pop_tok())

    def parse_tuple(self) -> Node.LiteralTuple:
        self.check_pop('(')
        elems = self.parse_exprs()
        self.check_pop(')')
        return Node.LiteralTuple(elems)

    def parse_list(self) -> Node.LiteralList:
        self.check_pop('[')
        elems = self.parse_exprs()
        self.check_pop(']')
        return Node.LiteralList(elems)

    def parse_trailer(self) -> Node.Trailer:
        res = None
        if self.top.code == '(':
            self.check_pop('(')
            res = Node.TrailerCall(self.parse_exprs())
            self.check_pop(')')
        elif self.top.code == '[':
            self.check_pop('[')
            res = Node.TrailerIndex(self.parse_exprs())
            self.check_pop(']')
        elif self.top.code == '.':
            self.check_pop('.')
            res = Node.TrailerDot(self.pop_tok().code)

        return res

    def parse_exprs(self) -> List[Node.Expression]:
        if self.top.code in [')', ']', '}']:
            return []
        res = [self.parse_expr()]
        while self.top.code == ',':
            self.check_pop(',')
            res.append(self.parse_expr())

        return res


def parse(code):
    return Parser(code).parse().simplify()

if __name__ == '__main__':
    sim = parse('''
    a.append(1);''')
    print(sim)
