
def const_is_empty(ast):
    return len(ast) == 1

def const_list(ast):
    return ast[1:]

def var_is_empty(ast):
    return len(ast) == 1

def var_list(ast):
    return ast[1:]

def proc_is_empty(ast):
    return len(ast) == 1

def proc_list(ast):
    return ast[1:]
