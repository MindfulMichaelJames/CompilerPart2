from ply import lex
import os
import sys
from ply import yacc

tokens = ["ID", "BINARY_LITERAL", "WHITESPACE", "COMMENT"]

literals = ["A", "S", "M", "D", "=", "(", ")"]

lexerror = ""

t_BINARY_LITERAL = r'[-+]?[0-9]+'

start = "Program"

p_errors_list = []

l_errors_list = []

syntree = []

s_table = []

s_errors_list = []


def t_WHITESPACE(t):
    r'\s*(\p{P})?\s'
    t.lexer.lineno += t.value.count("\n") # line number tracking for exception handling
    return t

def t_COMMENT(t):
    r'/\*(.|[\r\n])*?\*/|(//.*)'
    # regex allows for /* */ and // comments but also allows extra *s in a multiline /* */ comment
    t.lexer.lineno += t.value.count("\n") # implement line number tracking for exception handling
    return t

def t_ID(t):
    r'[_a-z][_a-z0-9]*'
    return t

def t_error(t):
    l_errors_list.append("lexical error on line %s" % t.lexer.lineno)
    t.lexer.skip(1)

def p_program_statements(p):
    """Program : Statements"""
    p[0] = ("Program", p[1])


def p_statements(p):
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """Statement : ID '=' expression"""
    p[0] = ("=", ["ID," + p[1], p[3]])
    if p[1] in s_table:
        s_errors_list.append("semantic error on line %s" % p.lineno(1))
    else:
        s_table.append(p[1])     


def p_expression_plus(p):
    """expression : expression 'A' term"""
    p[0] = ("A", [p[1], p[3]])
    if "ID" in p[3]:
        if p[3] not in s_table:
            s_errors_list.append("semantic error on line %s" % p.lineno(2))


def p_expression_minus(p):
    """expression : expression 'S' term"""
    p[0] = ("S", [p[1], p[3]])
    if "ID" in p[3]:
        if p[3] not in s_table:
            s_errors_list.append("semantic error on line %s" % p.lineno(2))


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_multiply(p):
    """term : term 'M' factor"""
    p[0] = ("M", [p[1], p[3]])
    if "ID" in p[3]:
        if p[3] not in s_table:
            s_errors_list.append("semantic error on line %s" % p.lineno(2))


def p_term_divide(p):
    """term : term 'D' factor"""
    p[0] = ("D", [p[1], p[3]])
    if "ID" in p[3]:
        if p[3] not in s_table:
            s_errors_list.append("semantic error on line %s" % p.lineno(2))


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_expression(p):
    """factor : '(' expression ')'"""
    p[0] = p[2]


def p_factor_binary(p):
    """factor : BINARY_LITERAL"""
    p[0] = "BINARY_LITERAL," + p[1]


def p_factor_id(p):
    """factor : ID"""
    p[0] = "ID," + p[1]

def p_comment(p):
    """factor : COMMENT"""


#endrules

def p_error(p):
    global flag_for_error
    flag_for_error = 1

    if p is not None:
        if p.type=="WHITESPACE" or p.type=="COMMENT":
            parser.errok()
        elif len(p_errors_list)>0:
            for item in p_errors_list:
                if str(p.lineno) not in item:
                    errors_list.append("parse error on line %s" % p.lineno)
            parser.errok()
        else:
            p_errors_list.append("parse error on line %s" % p.lineno)
            parser.errok()


def generate_tree(source):
    result = parser.parse(source)
    return result

lexer = lex.lex()
parser = yacc.yacc()

def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            lexer.input(infile.read())
            infile.seek(0)
            syntree = generate_tree(infile.read())

main()
