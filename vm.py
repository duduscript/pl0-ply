from codegen import *

def get_op(code):
    return code[0]

def get_l(code):
    return code[1]

def get_m(code):
    return code[2]

def pl0(codes):
    pc = sp = ar = 0
    bp = 1
    flag = False
    stack = []
    for i in range(0,1000):
        stack.append(0)
    lever = []
    for i in range(0,20):
        lever.append(-1)
    lever[0] = 0

    def base(bar):
        b = bp
        for i in range(0,bar):
            b = stack[b-1];
        return b
    while pc < len(codes) and  ar >= 0:
        code = codes[pc]
        print (code)
        pc += 1
        op = get_op(code)
        l = get_l(code)
        m = get_m(code)
        if op == 'LIT':
            stack[sp] = m
            sp += 1
        elif op == 'OPR':
            if m == 'OPR_RET':
                sp = bp - 1
                bp = stack[sp+1]
                pc = stack[sp+2]
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
            stack[sp + 1] = bp
            stack[sp + 2] = pc
            bp = sp + 1
            pc = m
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

ast = pl0_parse('./sample/parser.pl0')
codegen(ast)
print(len(code))
for ins in code:
    print(ins)
pl0(code)