from codegen import *
import sys

def get_op(code):
    return code[0]

def get_l(code):
    return code[1]

def get_m(code):
    return code[2]

def pl0(codes):
    def base(bar):
        b = bp
        for i in range(0,bar):
            b = stack[b-1];
        return b

    pc,sp,ar,bp = 0,0,0,1
    flag = False
    stack = [0] * 1000
    lever = [-1] * 20
    lever[0] = 0
    while pc < len(codes) and  ar >= 0:
        code = codes[pc]
        print (code)
        pc += 1
        op,l,m = get_op(code),get_l(code),get_m(code)
        if op == 'LIT':
            stack[sp] = m
            sp += 1
        elif op == 'OPR':
            if m == 'OPR_RET':
                sp = bp - 1
                bp,pc = stack[sp+1],stack[sp+2]
                lever[ar] = -1
                ar -= 1
            elif m == 'OPR_NEG':
                stack[sp - 1] = - stack[sp - 1]
            elif m == 'OPR_ADD':
                sp -= 1
                stack[sp - 1] += stack[sp]
            elif m == 'OPR_SUB':
                sp -= 1
                stack[sp - 1] -= stack[sp]
            elif m == 'OPR_MUL':
                sp -= 1
                stack[sp - 1] *= stack[sp]
            elif m == 'OPR_DIV':
                sp -= 1
                stack[sp - 1] /= stack[sp]
            elif m == 'OPR_ODD':
                stack[sp - 1] = int(stack[sp - 1])%2
            elif m == 'OPR_MOD':
                sp -= 1
                stack[sp - 1] %= stack[sp]
            elif m == 'OPR_EQL':
                sp -= 1
                if stack[sp] == stack[sp -1]:
                    stack[sp - 1] = 1
                else:
                    stack[sp - 1] = 0
            elif m == 'OPR_NEQ':
                sp -= 1
                if stack[sp] == stack[sp - 1]:
                    stack[sp - 1] = 0
                else:
                    stack[sp - 1] = 1
            elif m == 'OPR_LSS':
                sp -= 1
                if stack[sp - 1] < stack[sp]:
                    stack[sp - 1] = 1
                else:
                    stack[sp - 1] = 0
            elif m == 'OPR_LEQ':
                sp -= 1
                if stack[sp - 1] <= stack[sp]:
                    stack[sp - 1] = 1
                else:
                    stack[sp - 1] = 0
            elif m == 'OPR_GTR':
                sp -= 1
                if stack[sp - 1] > stack[sp]:
                    stack[sp - 1] = 1
                else:
                    stack[sp - 1] = 0
            elif m == 'OPR_GEQ':
                sp -= 1
                if stack[sp - 1] >= stack[sp]:
                    stack[sp - 1] = 1
                else:
                    stack[sp - 1] = 0
            else:
                pass
        elif op == 'LOD':
            stack[sp] = stack[base(l)-1+m]
            sp +=1
        elif op == 'STO':
            sp -= 1
            stack[base(l)-1+m] = stack[sp]
        elif op == 'CAL':
            stack[sp] = base(l)
            stack[sp+1],stack[sp+2] = bp,pc
            bp,pc = sp + 1,m
            lever[ar] = sp
            for i in range(0,ar):
                lever[ar] -= lever[i]
            ar += 1
            lever[ar] = 3
        elif op == 'INC':
            sp += m
        elif op == 'JMP':
            pc = m
        elif op == 'JPC':
            sp -= 1
            if stack[sp] == 0:
                pc = m
        elif op == 'SIO_OUT':
            flag = True
        elif op == 'SIO_IN':
            flag = True
        else:
            print ("Error in code {0}".format(pc))
        print (pc,bp,sp,ar,stack[0:sp])
        if flag == True:
            if op == 'SIO_OUT':
                sp -= 1
                print (stack[sp])
            if op == 'SIO_IN':
                stack[sp] = input()
                sp += 1
            flag =False

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) != 2:
        print('Usage: python pl0.py filepath!')
        exit(1)
    ast = pl0_parse(sys.argv[1])
    codegen(ast)
    print(len(code))
    for ins in code:
        print(ins)
    pl0(code)
