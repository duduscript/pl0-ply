from ifelse_stmt import *
from stmt import *
from while_stmt import *
from block import *
from program import *
from declare import *
from assign_stmt import *
from call_stmt import *
from read_stmt import *
from write_stmt import *
from pl0yacc import *
from op import *

def getop(ast):
    return ast[0]

code = []
currlevel = 0
currM = {}
names = {}

def codegen(ast):
    global currlevel,currM,code
    op = getop(ast)
    if op == 'program':
        codegen(program_block(ast))
        code.append(('OPR', 0, 'OPR_RET'))
    elif op == 'block':
        if currlevel not in currM:
            currM[currlevel] = 0
        currM[currlevel] += 3
        code.append(('INC', 0, 3))
        codegen(const_dec(ast))
        codegen(var_dec(ast))
        codegen(proc_dec(ast))
        codegen(block_stmts(ast))
    elif op == 'const':
        if not const_is_empty(ast):
            for con in const_list(ast):
                names[con[0]] = ['const',con[1]]
    elif op == 'var':
        if not var_is_empty(ast):
            for var in var_list(ast):
                if not currlevel in currM:
                    currM[currlevel] = 0
                names[var] = ['var',currlevel,currM[currlevel]]
                currM[currlevel] += 1
            code.append(('INC',0,len(var_list(ast))))
    elif op == 'proc':
        if not proc_is_empty(ast):
            for proc in proc_list(ast):
                names[proc] = ['proc', currlevel, len(code) + 1]
                currlevel += 1
                tmpBegin = len(code)
                code.append(('JMP',0,0))
                codegen(procs[proc])
                code.append(('OPR',0,'OPR_RET'))
                currlevel -= 1
                code[tmpBegin] = ('JMP',0,len(code))
    elif op == ':=':
        codegen(assign_right(ast))
        lexeme = assign_left(ast)
        code.append(('STO',abs(names[lexeme][1]-currlevel),names[lexeme][2]))
    elif op == 'call':
        lexeme = call_proc(ast)
        code.append(('CAL',abs(names[lexeme][1]-currlevel),names[lexeme][2]))
    elif op == 'stmt':
        stmt = get_stmt(ast)
        if stmt is not None:
            codegen(stmt)
        next_stmt = get_next_stmt(ast)
        if next_stmt is not None:
            codegen(next_stmt)
    elif op == 'if':
        codegen(get_if_cond(ast))
        tmpBeginOne = len(code)
        stmt = get_if_then(ast)
        code.append(('JPC', 0, 0))
        codegen(stmt)
        code.append(('JMP',0,0))
        code[tmpBeginOne] = ('JPC',0,len(code))
    elif op == 'if-else':
        codegen(get_if_cond(ast))
        tmpBeginOne = len(code)
        code.append(('JPC', 0, 0))
        codegen(get_if_then(ast))
        tmpBeginTwo = len(code)
        code.append(('JMP', 0, 0))
        code[tmpBeginOne] = ('JPC', 0, len(code))
        codegen(get_if_else(ast))
        code[tmpBeginTwo] = ('JMP',0,len(code))
    elif op == 'while':
        tmpBeginOne = len(code)
        codegen(get_while_cond(ast))
        tmpBeginTwo = len(code)
        code.append(('JPC',0,0))
        codegen(get_while_stmt(ast))
        code.append(('JMP',0,tmpBeginOne))
        code[tmpBeginTwo] = ('JPC',0,len(code))
    elif op == 'read':
        lexeme = read_ident(ast)
        code.append(('STO',abs(names[lexeme][1]-currlevel),names[lexeme][2]))
    elif op == 'write':
        expr = write_expr(ast)
        codegen(expr)
        code.append(('STO_OUT',0,1))
    elif op == 'odd':
        pass
    elif op == '=':
        codegen(eql_left(ast))
        codegen(eql_right(ast))
        code.append(('OPR',0,'OPR_EQL'))
    elif op == '<>':
        codegen(neq_left(ast))
        codegen(neq_right(ast))
        code.append(('OPR',0,'OPR_NEQ'))
    elif op == '<':
        codegen(less_left(ast))
        codegen(less_right(ast))
        code.append(('OPR',0,'OPR_LESS'))
    elif op == '<=':
        codegen(leq_left(ast))
        codegen(leq_right(ast))
        code.append(('OPR',0,'OPR_LEQ'))
    elif op == '>':
        codegen(grt_left(ast))
        codegen(grt_right(ast))
        code.append(('OPR',0,'OPR_GTR'))
    elif op == '>=':
        codegen(grq_left(ast))
        codegen(grt_right(ast))
        code.append(('OPR',0,'OPR_GEQ'))
    elif op == '*':
        codegen(mul_left(ast))
        codegen(mul_right(ast))
        code.append(('OPR',0,'OPR_MUL'))
    elif op == '/':
        codegen(div_left(ast))
        codegen(div_right(ast))
        code.append(('OPR',0,'OPR_DIV'))
    elif op == '-':
        if len(ast) == 2:
            code.append(('OPR',0,'OPR_NEG'))
        else:
            codegen(minus_left(ast))
            codegen(minus_right(ast))
            code.append(('OPR',0,'OPR_SUB'))
    elif op == '+':
        codegen(plus_left(ast))
        codegen(plus_right(ast))
        code.append(('OPR',0,'OPR_ADD'))
    elif op == 'ident':
        lexeme = ast[1]
        if names[lexeme][0] == 'var':
            code.append(('LOD',abs(names[lexeme][1]-currlevel),names[lexeme][2]))
        elif names[lexeme][0] == 'const':
            code.append(('LIT',0,names[lexeme][1]))
        else:
            pass
    elif op == 'number':
        lexeme = ast[1]
        code.append(('LIT', 0, lexeme))
    else:
        pass
    return code

ast = pl0_parse()
for key in procs:
    print(key)
    print(procs[key])
codegen(ast)
print(len(code))
for ins in code:
    print(ins)