from ontology.builtins import len,append

def Main(operation, args):
    if operation == 'Array':
        return Array(args)
    if operation == 'Boolean':
        return Boolean()
    if operation == 'Bytearray':
        arg1 = args[0]
        arg2 = args[1]
        return Bytearray(arg1, arg2)
    if operation == 'Intger':
        return Intger()
    if operation == 'Returntype':
        arg1 = args[0]
        arg2 = args[1]
        arg3 = args[2]
        return Returntype(arg1, arg2, arg3)
    if operation == 'String':
        return String()
    return False

def Array(args):
    return len(args)

def Boolean():
    return True

def Bytearray(arg1, arg2):
    return arg1 == arg2

def Intger():
    return 10

def Returntype(arg1, arg2, arg3):
    list = []
    list.append(arg1)
    list.append(arg2)
    list.append(arg3)
    return list

def String():
    return "Hello World"
