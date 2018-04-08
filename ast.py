import sys, lexer

class Program(object):
    '''
    A Program class for representing the program. A program
    consists of declarations and statements.
    Singleton
    '''
    env = dict()

    def __init__(self, decls, stmts):
        self.decls = decls
        self.stmts = stmts


    def __str__(self):
        indent = 0
        prog = "int main () { \n"
        for decl in self.decls:
            if self.decls[decl].tp == lexer.Lexer.INT:
                prog += "\tint "
            elif self.decls[decl].tp == lexer.Lexer.FLOAT:
                prog += "\tfloat "
            elif self.decls[decl].tp == lexer.Lexer.BOOL:
                prog += "\tbool "

            prog += decl + '\n'

        for stmt in self.stmts:
            prog += stmt.__str__(indent) + '\n'

        prog += "}"

        return prog


class Declaration(object):
    '''
    A Declaration consists of a type and an identifier
    '''

    def __init__(self, tp, ident):
        self.ident = ident
        self.tp = tp

    def __str__(self):
        return "Need to fill in __str__;\n"

class Stmt(object):
    '''
    An absract base class for statements
	'''
    pass

class Semi(Stmt):
    '''
	A class for representing a semicolon
	'''
    def __str__(self):
        return "; \n"

class Assign(Stmt):
    '''
	   An assignment statement
       '''
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + self.ident + " = " + str(self.expr) + ';'

class Block(Stmt):
    '''
	   A Statement Block
	   '''
    def __init__(self, stmts):
        self.stmts = stmts

    def __str__(self, indent):
        block = "\t" * indent +"{ \n"
        for s in self.stmts:
            block = block + s.__str__(indent) + '\n'
        block += "\t" * indent + "}"
        return block

class WhileStatement(Stmt):
    '''
    A While Statement
    '''
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'while ' + str(self.expr) + '\n' + self.stmt.__str__(indent)

class IfStatement(Stmt):
    '''
    An If Statement
    '''

    def __init__(self, expr, stmt, elstmt):
        self.expr = expr
        self.stmt = stmt
        self.elstmt = elstmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'if ' + str(self.expr) + '\n' + self.stmt.__str__(indent)

class PrintStatement(Stmt):
    '''
    A Print Statement
    '''
    def __init__(self, stmt):
        self.stmt = stmt

    def __str__(self, indent):
        indent += 1
        return '\t' * indent + 'print(' + self.stmt.__str__() + ');'

class Expr(object):
    '''
    Base class for all expressions
    '''
    def __init__(self, left, right):
        self.left = left
        self.right = right

class TrueExpr(Expr):
    '''
    Class for True Expressions
    '''
    def __init__(self, Bool):
        Expr.__init__(self, None, None)
        self.Bool = Bool

    def __str__(self):
        return str(self.Bool)


class FalseExpr(Expr):
    '''
    Class for False Expressions
    '''

    def __init__(self, Bool):
        Expr.__init__(self, None, None)
        self.Bool = Bool

    def __str__(self):
        return str(self.Bool)

class IntLit(Expr):
    '''
    Represents an integer literal
    '''

    def __init__(self, val):
        Expr.__init__(self, None, None)
        self.val = int(val)

    def __str__(self):
        return str(self.val)

class FloatLit(Expr):
    '''
    Represents an float literal
    '''

    def __init__(self, val):
        Expr.__init__(self, None, None)
        self.val = val

    def __str__(self):
        return str(self.val)

class Ident(Expr):
    '''
    id is the name of the identifier from the
    parser.
    '''
    def __init__(self, id):
        Expr.__init__(self, None, None)
        self.id = id

    def __str__(self):
        return str(self.id)


class UnaryExpr(Expr):
    '''
    Base class for unary expressions
    '''
    def __init__(self, expr):
        Expr.__init__(self, None, None)
        self.expr = expr


class NegExpr(UnaryExpr):
    '''
    A negation expression
    '''
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)

    def __str__(self):
        return '-' + '(' + str(self.expr) + ')'


class NotExpr(UnaryExpr):
    '''
    A not unary expression
    '''
    def __init__(self, expr):
        UnaryExpr.__init__(self, expr)

    def __str__(self):
        return '!' + '(' + str(self.expr) + ')'


class OpExpr(Expr):
    '''
    The Abstract Syntax for a Binary Operation Expression
    '''
    def __init__(self, left, right, op):
        Expr.__init__(self,left,right)
        self.op = op

    def __str__(self):
        return "(" + str(self.left) + ' ' + str(self.op) + ' ' + str(self.right) + ")"


# main program to test some of the classes above
if __name__ == "__main__":

    # represent a + 55
    expr = OpExpr(Ident('a'), IntLit(55), '+')
    print(expr)

    # (a + c) * 99
    expr2 = OpExpr(OpExpr(Ident('a'), Ident('c'), '+'), IntLit(99), '+')
    print(expr2)

    # (a+55) + ((a+c) * 99)
    expr3 = OpExpr(expr, expr2, '*')
    print(expr3)









