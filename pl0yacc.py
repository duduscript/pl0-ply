import ply.yacc as yacc
import ply.lex as lex
from pl0lex import *

procs = {}
ast = []

def p_program(p):
    'program : block period_token'
    #  |         |         |
    # p[0]      p[1]     p[2]
    global ast
    p[0] = ['program',p[1]]
    ast = p[0]
    print(p[0])

def p_block(p):
    'block : con_dec var_dec proc_dec stmt'
    p[0] = ["block",p[1],p[2],p[3],p[4]]

def p_con_dec(p):
    '''con_dec : const_token ident_token eql_token number_token con_dec_cdr semicolom_token
               | empty
    '''
    p[0] = ['const']
    if len(p) != 2:
        p[0].append([p[2],p[4]])
        p[0] += p[5]

def p_con_dec_cdr(p):
    '''con_dec_cdr : comma_token ident_token eql_token number_token con_dec_cdr
                   | empty
    '''
    p[0] = []
    if len(p) != 2:
        p[0].append([p[2],p[4]])
        p[0] += p[5]

def p_var_dec(p):
    '''var_dec : var_token ident_token var_dec_cdr semicolom_token
               | empty
    '''
    p[0] = ['var']
    if len(p) != 2:
        p[0].append(p[2])
        p[0] += p[3]

def p_var_dec_cdr(p):
    '''var_dec_cdr : comma_token ident_token var_dec_cdr
                   | empty
    '''
    p[0] = []
    if len(p) != 2:
        p[0].append(p[2])
        p[0] += p[3]

def p_proc_dec(p):
    '''proc_dec : proc_token ident_token semicolom_token block semicolom_token proc_dec_cdr
                | empty
    '''
    p[0] = ['proc']
    if len(p) != 2:
        p[0].append(p[2])
        procs[p[2]] = p[4]
        p[0] += p[6]

def p_proc_dec_cdr(p):
    '''proc_dec_cdr : proc_token ident_token semicolom_token block semicolom_token proc_dec_cdr
                    | empty
    '''
    p[0] = []
    if len(p) != 2:
        p[0].append(p[2])
        procs[p[2]] = p[4]
        p[0] += p[6]

def p_stmt(p):
    '''stmt : assign_stmt
            | call_stmt
            | begin_stmt
            | if_stmt
            | while_stmt
            | read_stmt
            | write_stmt
            | empty
    '''
    p[0] = p[1]

def p_assign_stmt(p):
    'assign_stmt : ident_token become_token expr'
    p[0] = [':=',p[1],p[3]]

def p_call_stmt(p):
    'call_stmt : call_token ident_token'
    p[0] = ['call',p[2]]

def p_begin_stmt(p):
    'begin_stmt : begin_token stmt begin_stmt_cdr end_token'
    p[0] = ['stmt',p[2],p[3]]

def p_begin_stmt_cdr(p):
    '''begin_stmt_cdr : semicolom_token stmt begin_stmt_cdr
                      | empty
    '''
    if len(p) != 2:
        p[0] = ['stmt',p[2],p[3]]

def p_if_stmt(p):
    '''if_stmt : if_token cond then_token stmt
               | if_token cond then_token stmt else_token stmt
    '''
    if len(p) == 5:
        p[0] = ['if',p[2],p[4]]
    else:
        p[0] = ['if-else',p[2],p[4],p[6]]

def p_while_stmt(p):
    'while_stmt : while_token cond do_token stmt'
    p[0] = ['while',p[2],p[4]]

def p_read_stmt(p):
    'read_stmt : read_token ident_token'
    p[0] = ['read',p[2]]

def p_write_stmt(p):
    'write_stmt : write_token expr'
    p[0] = ['write',p[2]]

def p_cond(p):
    '''cond : odd_token expr
            | expr cmp expr
    '''
    if len(p) == 3:
        p[0] = ['odd',p[2]]
    else:
        p[0] = [p[2],p[1],p[3]]

def p_cmp(p):
    '''cmp : eql_token
           | les_token
           | leq_token
           | grt_token
           | geq_token
           | neq_token
    '''
    p[0] = p[1]

def p_expr_flag(p):
    '''expr : flag no_flag_expr
            | no_flag_expr
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '+':
        p[0] = p[2]
    else:
        p[0] = ['-',p[2]]

def p_expr_no_flag(p):
    '''no_flag_expr : term plus_token term
       no_flag_expr : term minus_token term
       no_flag_expr : term
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = ['+',p[1],p[3]]
    else:
        p[0] = ['-',p[1],p[3]]

def p_flag(p):
    '''flag : plus_token
            | minus_token
    '''
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_term_mul(p):
    '''term : factor mul_token term
       term : factor divide_token term
    '''
    if(p[2] == '*'):
        p[0] = ['*',p[1],p[3]]
    else:
        p[0] = ['/',p[1],p[3]]

def p_factor_ident(p):
    'factor : ident_token'
    p[0] = ['ident',p[1]]

def p_factor_number(p):
    'factor : number_token'
    p[0] =  ['number',p[1]]

def p_factor_expr(p):
    'factor : lparent_token expr rparent_token'
    p[0] = p[2]

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    print("Error in line {0}".format(p))

# Test it out

def print_tokens(lexer):
    for token in lexer:
        print token

def pl0_lexer(data):
    lexer = lex.lex()
    lexer.input(data)
    print_tokens(lexer)

def pl0_parse():
    with open('./sample/parser.pl0') as file:
        data = file.read()
    pl0_lexer(data)
    y = yacc.yacc()
    y.parse(data)
    print(procs)
    return ast

pl0_parse()