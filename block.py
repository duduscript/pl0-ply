def const_dec(ast):
    return ast[1]

def var_dec(ast):
    return ast[2]

def proc_dec(ast):
    return ast[3]

def block_stmts(ast):
    return ast[4]