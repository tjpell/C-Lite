import re
import sys

#----------------------------
def counter():
    '''
    :return: a generator for counting
    '''

    i = 0
    while True:
        yield i
        i = i + 1


class Lexer(object):
    '''
    Our Lexer class for classifying tokens.
    '''

    # list of token constants
    cnt = counter()
    FILE_NOT_FOUND_ERROR = next(cnt)
    PLUS = next(cnt)
    LPAREN = next(cnt)
    RPAREN = next(cnt)
    INTLIT = next(cnt)
    FLOATLIT = next(cnt)
    BOOL = next(cnt)
    ID     = next(cnt)
    EQ_EQ  = next(cnt)
    EQ     = next(cnt)
    MINUS  = next(cnt)
    TIMES  = next(cnt)
    DIV    = next(cnt)
    OR     = next(cnt)
    AND    = next(cnt)
    NEQ    = next(cnt)
    LTEQ   = next(cnt)
    LT     = next(cnt)
    GTEQ   = next(cnt)
    GT     = next(cnt)
    MOD    = next(cnt)
    NOT    = next(cnt)
    SEMI    = next(cnt)
    COM    = next(cnt)
    LCBRACK = next(cnt)
    RCBRACK = next(cnt)
    LBRACK = next(cnt)
    RBRACK = next(cnt)
    REALNUM = next(cnt)
    STR    = next(cnt)
    KEY    = next(cnt)
    PRINT = next(cnt)
    IF = next(cnt)
    WHILE = next(cnt)
    INT = next(cnt)
    FLOAT = next(cnt)
    MAIN = next(cnt)
    ELSE = next(cnt)
    TRUELIT = next(cnt)
    FALSELIT = next(cnt)
    POWER = next(cnt)
    END_OF_FILE = next(cnt)


    # token dictionary for punctuation and operators
    td = {
        '+' : PLUS,
        '==': EQ_EQ,
        '=' : EQ,
        '(' : LPAREN,
        ')' : RPAREN,
        '-' : MINUS,
        '#' : POWER,
        '*' : TIMES,
        '/' : DIV,
        '||': OR,
        '&&': AND,
        '!=': NEQ,
        '<=': LTEQ,
        '<' : LT,
        '>=': GTEQ,
        '>' : GT,
        '%' : MOD,
        '!' : NOT,
        ';' : SEMI,
        ',' : COM,
        '{' : LCBRACK,
        '}' : RCBRACK,
        '[' : LBRACK,
        ']' : RBRACK,
        'intlit' : INTLIT,
        'floatlit' : FLOATLIT,
        'true' : TRUELIT,
        'false' : FALSELIT,
        'int' : INT,
        'float' : FLOAT,
        'main' : MAIN,
        'bool' : BOOL,
        'key' : KEY,
        'id' : ID,
        'while' : WHILE,
        'if' : IF,
        'print' : PRINT,
        'End of File' : END_OF_FILE
    }

    # Map from token values to token names
    name = {
        '+': "PlUS",
        '==': "EQ-EQ",
        '=' : 'EQUAL',
        '(': 'LPAREN',
        ')' : 'RPAREN',
        '-': 'MINUS',
        '#' : 'POWER',
        '*' : 'TIMES',
        '/' : 'DIVIDE',
        '||' : 'OR',
        '&&' : 'AND',
        '!=' : 'NEQ',
        '<' : 'LT',
        '<=' : 'LEQ',
        '>' : 'GT',
        '>=' : 'GEQ',
        '%' : 'MOD',
        '!' : 'NOT',
        ';' : 'SEMI',
        ',' : 'COMMA',
        '{' : 'LBRACE',
        '}' : 'RBRACE',
        '[' : 'LBRACK',
        ']' : 'RBRACK'
    }

    # regex patterns for splitting a line
    split_patt = re.compile(
        '''
           \s   |       # whitespace
           (".*?") | # String
           ("\@")    |  # Comment
           (\() |       # left paren
           (\)) |       # right paren
           (\+) |       # plus
           (\-) |       # minus
           (\{) |       # left brace
           (\}) |       # right brace
           (\,) |       # comma
           (\=\=)|      # equal comparator
           (\=) |       # equal
           (\*) |       # times
           (\|\|) |     # or
           (\&\&) |     # and
           (\/) |       # divide
           (\!\=) |     # not equal
           (\<\=) |     # less than or equal to
           (\<) |       # less than
           (\>\=) |     # greater than or equal to
           (\>) |       # greater than
           (\%) |       # mod
           (\!) |       # not
           (\;) |       # colon
           (\[) |       # left bracket
           (\])         # right bracket
                   ''', re.VERBOSE)

    # regex for an identifier
    id_patt = re.compile("^[a-zA-Z_]\w*$")

    # regex for an integer
    int_patt = re.compile("^\d+$")

    # regex for a real number
    real_patt = re.compile("^\d+\.\d+$")

    #regex for string
    str_patt = re.compile('\"(.+?)\"')

    # regex for comment
    com_patt = re.compile("@")

    # regex for keyword
    key_patt = re.compile("^bool$|^else$|^false$|^if$|^true$|^float$|^int$|^while$|^print$")


    def token_generator(self,filename):
        '''
        Our token generator.
        :param filename: name of course program file
        :return: a generator
        '''
        try:
            file = open(filename)
        except IOError:
            print("File "+ filename+ " not found")
            yield (Lexer.FILE_NOT_FOUND_ERROR, "Cannot open file")
            sys.exit()

        count = counter()
        lineNumber = next(count)
        # for every line in the file
        for line in file:
            line = line.replace("//", '@')
            line = line.replace("**", '#')
            # split a line based on our split pattern and filter
            # all of the empty strings and None values.
            tokens = Lexer.split_patt.split(line)
            tokens = [x for x in tokens if x]

            # for each possible token in the line
            for tok in tokens:
                v = Lexer.td.get(tok, False)
                if v:
                    yield (Lexer.td[tok], tok, lineNumber+1)
                elif Lexer.key_patt.search(tok):
                    yield (Lexer.td['key'], tok, lineNumber+1)
                elif Lexer.id_patt.search(tok):
                    yield (Lexer.td['id'], tok, lineNumber+1)
                elif Lexer.int_patt.search(tok):
                    yield (Lexer.td['intlit'], tok, lineNumber+1)
                elif Lexer.real_patt.search(tok):
                    yield (Lexer.td['floatlit'], tok, lineNumber+1)
                elif Lexer.str_patt.search(tok):
                    tok = tok.replace('@', '//')
                    yield (Lexer.td[tok], tok, lineNumber + 1)
                elif Lexer.com_patt.search(tok):
                    break
                else:
                    yield ("Unrecognized character", str(tok), "on line " + str(lineNumber+1))
            lineNumber += 1

        #while True:
        yield (Lexer.END_OF_FILE, Lexer.END_OF_FILE, Lexer.END_OF_FILE)
