def Main(operation, args):
    if operation == 'While':
        a = args[0]
        return While(a)
    if operation == 'ifelse':
        a = args[0]
        b = args[1]
        return ifelse(a, b)
    return False


def While(a):
    b = 0
    i = 0
    while i < a:
        b = b + i
        i = i + 1
    return b


def ifelse(a, b):
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0
