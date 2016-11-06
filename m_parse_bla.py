from ply import yacc
from lex_bla import tokens
import sys

# full specification of the grammar:
# statement     -> ID = expression
# expression    -> expression 'A' term
#               -> expression 'S' term
#               -> term
# term          -> term 'M' factor
#               -> term 'D' factor
#               -> factor
# factor        -> '(' expression ')'
#               -> BINARY_LITERAL
#               -> ID
def p_program(p):
    ''' program : statement program
                | statement'''
    p[0] = ["Program"] + [p[k] for k in range(1, len(p))]

def p_statement(p):
    '''statement : ID '=' expression '''
    p[0] = [p[2], ['ID',p[1]], p[3]]

def p_expression_3(p):
    '''expression : expression 'A' term
                  | expression 'S' term'''
    # expressions with three elements
    p[0] = [p[2], p[1], p[3]]

def p_expression_1(p):
    '''expression : term'''
    # expressions with one elements
    p[0] = p[1]

def p_term_3(p):
    ''' term : term 'M' factor
             | term 'D' factor '''
    # terms with three elements
    p[0] = [p[2], p[1], p[3]]

def p_term_1(p):
    ''' term : factor'''
    # terms with one element
    p[0] = p[1]

def p_factor_parentheses(p):
    ''' factor : '(' expression ')' '''
    # handle parentheses
    p[0] = p[2]

def p_factor_binary(p):
    ''' factor : BINARY_LITERAL '''
    p[0] = ["BINARY_LITERAL",p[1]]

def p_factor_id(p):
    ''' factor : ID '''
    p[0] = ["ID",p[1]]

# handle errors
def p_error(p):
    if p: # not EOF
        if p.type=="WHITESPACE" or p.type=="COMMENT":
            parser.errok()
        else:
            print("Syntax error found with the", p.type, "token:", p.value)
    else:
        print("Error: Unexpected EOF encountered")


# functions for printing the abstract syntax tree
def recursive_descend(ast, out_file, depth):
    '''Recursive helper function to descend_and_write;
    recursively descends the given ast, writing the result to the out_file
    as a flat text tree'''
    # possible values or ast[0]:
    # Program -> start of a Program
    # ID -> ast[1] is an identifier
    # BINARY_LITERAL -> ast[1] is a binary value
    # = -> ast[1] is an ['ID', identifier], ast[2] is an expression
    # A|S|M|D -> ast[1], ast[2] are operands
    if ast[0] == "Program":
        print('Program', file=out_file, end='\n')
        for node in ast:
            recursive_descend(node, out_file, depth+1)
    elif ast[0] == "ID" or ast[0] == "BINARY_LITERAL":
        print('\t'*depth, file=out_file, end='') # push to correct depth using tabs
        print(ast[0] + "," + ast[1], file=out_file, end='\n')
    else: # ast[0] is one of A,S,M,D,=
        print('\t'*depth, file=out_file, end='') # push to correct depth using tabs
        print(ast[0], file=out_file, end='\n')
        recursive_descend(ast[1], out_file, depth+1) # left child
        recursive_descend(ast[2], out_file, depth+1) # right child

def descend_and_write(ast, out_file):
    ''' Descend the given AST, writing the results in flat text to
    the given output file'''
    recursive_descend(ast, out_file, 0)


#build the parser
parser = yacc.yacc()

# get input file name
input_filename = sys.argv[1]
file_in = open(input_filename, mode='r')
data = ''
for s in file_in.readlines():
    data += s
file_in.close()

#open .ast output file
output_filename = input_filename[:input_filename.rfind('.')] + '.ast'
file_out = open(output_filename, mode='w')

# run the parser
result = parser.parse(data)
#descend_and_write(result, file_out)

file_out.close()
