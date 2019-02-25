def Main(operation, args):
    if operation == 'Add':
        a = args[0]
        b = args[1]
        return Add(a, b)
    if operation == 'And':
        a = args[0]
        b = args[1]
        return And(a, b)
    if operation == 'Divide':
        a = args[0]
        b = args[1]
        return Divide(a, b)
    if operation == 'eq':
        a = args[0]
        b = args[1]
        return eq(a, b)
    if operation == 'lq':
        a = args[0]
        b = args[1]
        return lq(a, b)
    if operation == 'leftshift':
        a = args[0]
        b = args[1]
        return leftshift(a, b)
    if operation == 'lr':
        a = args[0]
        b = args[1]
        return lr(a, b)
    if operation == 'mode':
        a = args[0]
        b = args[1]
        return mode(a, b)
    if operation == 'multi':
        a = args[0]
        b = args[1]
        return multi(a, b)
    if operation == 'ne':
        a = args[0]
        b = args[1]
        return ne(a, b)
    if operation == 'ng':
        a = args[0]
        return ng(a)
    if operation == 'Or':
        a = args[0]
        b = args[1]
        return Or(a, b)
    if operation == 'rightshift':
        a = args[0]
        b = args[1]
        return rightshift(a, b)
    if operation == 'se':
        a = args[0]
        b = args[1]
        return se(a, b)
    if operation == 'selfadd':
        a = args[0]
        return selfadd(a)
    if operation == 'selfsub':
        a = args[0]
        return selfsub(a)
    if operation == 'sl':
        a = args[0]
        b = args[1]
        return sl(a, b)
    if operation == 'sub':
        a = args[0]
        b = args[1]
        return sub(a, b)
    return False


def Add(a, b):
    return a + b


def And(a, b):
    return a and b


def Divide(a, b):
    return a / b


def eq(a, b):
    return a == b


def lq(a, b):
    return a >= b


def leftshift(a, b):
    return a << b


def lr(a, b):
    return a > b


def mode(a, b):
    return a % b


def multi(a, b):
    return a * b


def ne(a, b):
    return a != b


def ng(a):
    b = not a
    return b


def Or(a, b):
    return a or b


def rightshift(a, b):
    return a >> b


def se(a, b):
    return a <= b


def selfadd(a):
    a += 1
    return a


def selfsub(a):
    a -= 1
    return a


def sl(a, b):
    return a < b


def sub(a, b):
    return a - b
