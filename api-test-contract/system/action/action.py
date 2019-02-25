from ontology.interop.System.Action import RegisterAction
from ontology.interop.System.Runtime import Notify

Transfer = RegisterAction('test','a')


def Main(operation, args):
    if operation == "test":
        return test()
    return False

def test():
    a = 1
    Transfer(a)
    return True