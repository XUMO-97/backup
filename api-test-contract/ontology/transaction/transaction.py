from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Transaction import GetType,GetAttributes
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.interop.System.Blockchain import GetBlock
from ontology.interop.System.Block import GetTransactionByIndex,GetTransactionCount


def Main(operation, args):
    if operation == 'getType':
        return getType()
    if operation == 'getAttributes':
        return getAttributes()
    return False

def getType():
    Hash = GetCurrentBlockHash()
    block = GetBlock(Hash)
    tx = GetTransactionByIndex(block ,0)
    Type = GetType(tx)
    Notify(Hash)
    Notify(Type)
    return True

def getAttributes():
    Hash = GetCurrentBlockHash()
    block = GetBlock(Hash)
    count = GetTransactionCount(block)
    Notify(count)
    if count != None:
        tx = GetTransactionByIndex(block ,0)
        attr = GetAttributes(tx)
        Notify(tx)
        return True
    return False