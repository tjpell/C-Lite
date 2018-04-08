import lexer
import ast
import sys


class Parser(object):

    # the first-set of the Type non-terminal
    type_first = {lexer.Lexer.INT, lexer.Lexer.FLOAT,
                  lexer.Lexer.BOOL}

    stmt_first = { lexer.Lexer.SEMI,
                 lexer.Lexer.LCBRACK,
                 lexer.Lexer.ID,
                 lexer.Lexer.IF,
                 lexer.Lexer.WHILE,
                 lexer.Lexer.PRINT}

    EquOp_first = { lexer.Lexer.EQ_EQ,
                    lexer.Lexer.NEQ}

    RelOp_first = { lexer.Lexer.GT,
                    lexer.Lexer.GTEQ,
                    lexer.Lexer.LT,
                    lexer.Lexer.LTEQ}

    addOp_first = { lexer.Lexer.PLUS,
                    lexer.Lexer.MINUS}

    mulOp_first = { lexer.Lexer.TIMES,
                    lexer.Lexer.DIV,
                    lexer.Lexer.MOD}

    unaryOp_first = { lexer.Lexer.NOT,
                    lexer.Lexer.MINUS}

    # need to add print keyword to lexer

    def __init__(self, filename):
        self.lexer = lexer.Lexer()
        self.lex = self.lexer.token_generator(filename)
        self.curr_tok = next(self.lex)

    def parse(self):
        '''
        :return: ast.Program
        '''
        prog = self.program()

        if self.curr_tok[0] != lexer.Lexer.END_OF_FILE:
            raise Exception("Extra symbols in input")

        return prog

    def program(self):

        # match int main ( ) {
        if self.curr_tok[0] != lexer.Lexer.INT:
            print("'int' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)
        self.curr_tok = next(self.lex)

        if self.curr_tok[0] != lexer.Lexer.MAIN:
            print("'main' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)
        self.curr_tok = next(self.lex)

        if self.curr_tok[0] != lexer.Lexer.LPAREN:
            print("'(' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)
        self.curr_tok = next(self.lex)

        if self.curr_tok[0] != lexer.Lexer.RPAREN:
            print("')' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)
        self.curr_tok = next(self.lex)

        if self.curr_tok[0] != lexer.Lexer.LCBRACK:
            print("'{' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        self.decls = self.declarations()
        self.stmts = self.statements()

        if self.curr_tok[0] != lexer.Lexer.RCBRACK:
            print("'}' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)
        self.curr_tok = next(self.lex)

        return ast.Program(self.decls, self.stmts)

    def declarations(self):
        '''
        Declarations --> { Declaration }
        :return: list of declaration objects
        '''
        decls = dict()
        while self.curr_tok[0] in Parser.type_first:

            decl = self.declaration()
            decls[decl.ident] = decl

        return decls

    def declaration(self):
        '''
        Declaration --> Type  Identifier  ;
        :return: Declaration object
        '''
        t = self.type()

        # match a semi
        if self.curr_tok[0] != lexer.Lexer.SEMI:
            print("Error: semicolon expected found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)
        return t

    def type(self):
        if self.curr_tok[0] in Parser.type_first:
            tp = self.curr_tok[0]
            self.curr_tok = next(self.lex)
        else:
            print("Error: 'int', 'bool', or 'float' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        # we should be at an identifier
        if self.curr_tok[0] != lexer.Lexer.ID:
            print("Error: identifier expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        tmp = self.curr_tok
        self.curr_tok = next(self.lex)
        return ast.Declaration(tp,tmp[1])

    def statements(self):
        '''
        Statements --> { Statement }
        :return: list of statement objects
        '''
        stmts = []
        while self.curr_tok[0] in Parser.stmt_first:
            stmts.append(self.statement())

        return stmts

    def statement(self):
        if self.curr_tok[0] in Parser.stmt_first:
            if self.curr_tok[0] == lexer.Lexer.SEMI:
                return ast.Semi
            elif self.curr_tok[0] == lexer.Lexer.LCBRACK:
                return self.block()
            elif self.curr_tok[0] == lexer.Lexer.ID:
                return self.assignment()
            elif self.curr_tok[0] == lexer.Lexer.IF:
                return self.ifStatement()
            elif self.curr_tok[0] == lexer.Lexer.WHILE:
                return self.whileStatement()
            elif self.curr_tok[0] == lexer.Lexer.PRINT:
                return self.printStatement()
        else:
            print("Error: statement expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

    def block(self):
        '''
        Block --> { Statement }
        :return: ast.Block
        '''
        # need '{'
        if self.curr_tok[0] != lexer.Lexer.LCBRACK:
            print("Error: '{' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        stmt = self.statements()


        # need '}'
        if self.curr_tok[0] != lexer.Lexer.RCBRACK:
            print("Error: '}' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        return ast.Block(stmt)

    def assignment(self):
        '''
        Assignment -> id = Expression ;
        :return: ast.Assign
        '''
        tmpid = self.curr_tok
        if tmpid[1] not in self.decls:
            print("Error: Identifier", self.curr_tok[1], "not declared on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)
        if self.curr_tok[0] != lexer.Lexer.EQ:
            print("Error: '=' expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        expr = self.expr()

        if self.curr_tok[0] != lexer.Lexer.SEMI:
            print("Error: semicolon expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        return ast.Assign(tmpid[1], expr)

    def ifStatement(self):
        '''
        IfStatement --> if "(" Expression ")" Statement [ else Statement ]
        :return: ast.IfStatement
        '''

        # need keyword 'if'
        if self.curr_tok[0] != lexer.Lexer.IF:
            print("Error: 'if' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need '('
        if self.curr_tok[0] != lexer.Lexer.LPAREN:
            print("Error: '(' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need Expression
        expr = self.expr()

        # need ')'
        if self.curr_tok[0] != lexer.Lexer.RPAREN:
            print("Error: ')' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need Statement
        stmt = self.statement()
        elsstmt = None

        # else statements
        if self.curr_tok[0] == lexer.Lexer.ELSE: # if we have 'else'
            self.curr_tok[0] = next(self.lex)
            elsstmt = self.statement()

        return ast.IfStatement(expr, stmt, elsstmt)


    def whileStatement(self):
        '''
        WhileStatement --> while "(" Expression ")" Statement
        :return: ast.whileStatement
        '''

        # need keyword 'while'
        if self.curr_tok[0] != lexer.Lexer.WHILE:
            print("Error: 'while' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need '('
        if self.curr_tok[0] != lexer.Lexer.LPAREN:
            print("Error: '(' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need Expression
        expr = self.expr()

        # need ')'
        if self.curr_tok[0] != lexer.Lexer.RPAREN:
            print("Error: ')' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need Statement
        stmt = self.statement()

        return ast.WhileStatement(expr, stmt)

    def printStatement(self):
        '''
        Print --> print '(' Expression ')' ;
        :return: ast.PrintStatement
        '''

        # need keyword 'print'
        if self.curr_tok[0] != lexer.Lexer.PRINT:
            print("Error: 'print' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need '('
        if self.curr_tok[0] != lexer.Lexer.LPAREN:
            print("Error: '(' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        # need Expression
        expr = self.expr()

        # need ')'
        if self.curr_tok[0] != lexer.Lexer.RPAREN:
            print("Error: ')' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        if self.curr_tok[0] != lexer.Lexer.SEMI:
            print("Error: semicolon expected: found", self.curr_tok[1], "on line", self.curr_tok[2])
            sys.exit(1)

        self.curr_tok = next(self.lex)

        return ast.PrintStatement(expr)

    def expr(self):
        '''
        Expression --> Conjunction { || Conjunction }
        :return: ast.expr
        '''
        left_tree = self.conj()

        while self.curr_tok[0] == lexer.Lexer.OR: # While we have ||
            self.curr_tok = next(self.lex)
            right_tree = self.conj()
            left_tree = ast.OpExpr(left_tree, right_tree, "||")
        return left_tree

    def conj(self):
        '''
        Conjunction --> Equality { && Equality }
        :return: ast.conj
        '''
        left_tree = self.equality()

        while self.curr_tok[0] == lexer.Lexer.AND:
            self.curr_tok = next(self.lex)
            right_tree = self.equality()
            left_tree = ast.OpExpr(left_tree, right_tree, "&&")
        return left_tree

    def equality(self):
        '''
        Equality --> Relation [ EquOp Addition ] 
        :return: ast.equality
        '''
        left_tree = self.relat()

        if self.curr_tok[0] in Parser.EquOp_first:
            if self.curr_tok[0] == lexer.Lexer.EQ_EQ:
                self.curr_tok = next(self.lex)
                right_tree = self.relat()
                left_tree = ast.OpExpr(left_tree, right_tree, "==")
            else:
                self.curr_tok[0] = next(self.lex)
                right_tree = self.relat()
                left_tree = ast.OpExpr(left_tree, right_tree, "!=")
        return left_tree

    def relat(self):
        '''
        Relation --> Addition [ RelOp Addition ]
        :return: ast.relation
        '''
        left_tree = self.addition()

        if self.curr_tok[0] in Parser.RelOp_first:
            if self.curr_tok[0] == lexer.Lexer.GT:
                self.curr_tok = next(self.lex)
                right_tree = self.addition()
                left_tree = ast.OpExpr(left_tree, right_tree, ">")
            elif self.curr_tok[0] == lexer.Lexer.GTEQ:
                self.curr_tok = next(self.lex)
                right_tree = self.addition()
                left_tree = ast.OpExpr(left_tree, right_tree, ">=")
            elif self.curr_tok[0] == lexer.Lexer.LT:
                self.curr_tok = next(self.lex)
                right_tree = self.addition()
                left_tree = ast.OpExpr(left_tree, right_tree, "<")
            else:
                self.curr_tok = next(self.lex)
                right_tree = self.addition()
                left_tree = ast.OpExpr(left_tree, right_tree, "<=")
        return left_tree

    def addition(self):
        '''
        Addition --> Term { AddOp Term }
        :return: ast.add
        '''
        left_tree = self.term()

        while self.curr_tok[0] in Parser.addOp_first:  # while we have an AddOp
            if self.curr_tok[0] == lexer.Lexer.PLUS:
                self.curr_tok = next(self.lex)
                right_tree = self.term()
                left_tree = ast.OpExpr(left_tree,right_tree, "+")
            else:
                self.curr_tok = next(self.lex)
                right_tree = self.term()
                left_tree = ast.OpExpr(left_tree, right_tree, "-")
        return left_tree

    def term(self):
        '''
        Term --> ExpOp { MulOp ExprOp }
        :return: ast.Expr
        '''
        left_tree = self.ExpOp()
        while self.curr_tok[0] in Parser.mulOp_first:  # while we have an MulOp
            if self.curr_tok[0] == lexer.Lexer.TIMES:
                self.curr_tok = next(self.lex)
                right_tree = self.ExpOp()
                left_tree = ast.OpExpr(left_tree, right_tree, "*")
            elif self.curr_tok[0] == lexer.Lexer.DIV:
                self.curr_tok = next(self.lex)
                right_tree = self.ExpOp()
                left_tree = ast.OpExpr(left_tree, right_tree, "/")
            else:
                self.curr_tok = next(self.lex)
                right_tree = self.ExpOp()
                left_tree = ast.OpExpr(left_tree, right_tree, "%")

        # what is true if we get here
        return left_tree

    def ExpOp(self):
        left = self.fact()
        if self.curr_tok[0] == lexer.Lexer.POWER:
            self.curr_tok = next(self.lex)
            right = self.ExpOp()
            left = ast.OpExpr(left, right, '**')
        return left

    def fact(self):
        '''
        Factor --> [ UnaryOp ] Primary
        :return: ast.fact
        '''
        if self.curr_tok[0] in Parser.unaryOp_first:
            if self.curr_tok[0] == lexer.Lexer.MINUS:
                self.curr_tok = next(self.lex)
                expr = ast.NegExpr(self.prim())
            else:
                self.curr_tok = next(self.lex)
                expr = ast.NotExpr(self.prim())
        else:
            expr = self.prim()
        return expr


    def prim(self):

        temp = self.curr_tok
        self.curr_tok = next(self.lex)
        if temp[0] == lexer.Lexer.ID:
            # make sure ID is declared in self.decls
            if temp[1] not in self.decls:
                print("Error: Identifier", temp[1], "not declared on line", self.curr_tok[2])
                sys.exit(1)
            return ast.Ident(temp[1])
        elif temp[0] == lexer.Lexer.INTLIT:
            return ast.IntLit(int(temp[1]))

        elif temp[0] == lexer.Lexer.FLOATLIT:
            return ast.FloatLit(float(temp[1]))

        elif temp[0] == lexer.Lexer.TRUELIT:
            return ast.TrueExpr(temp[1])

        elif temp[0] == lexer.Lexer.FALSELIT:
            return ast.FalseExpr(temp[1])

        elif temp[0] == lexer.Lexer.LPAREN:
            tree = self.expr()
            if self.curr_tok[0] == lexer.Lexer.RPAREN:
                self.curr_tok = next(self.lex)
                return tree
            else:
                print("Error: ')' expected found:", self.curr_tok[1], "on line", self.curr_tok[2])
                sys.exit(1)

        else:
            print("Error: syntax error: unexpected input", self.curr_tok[1], " on line:", self.curr_tok[2])
            sys.exit(1)

# main program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        testFile = sys.argv[1]
    else:
        sys.exit("No file specified")

    p = Parser(testFile)
    t = p.parse()
    print(t)




