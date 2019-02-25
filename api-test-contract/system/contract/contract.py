from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Blockchain import GetContract
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.System.Contract import GetStorageContext
from ontology.interop.System.Contract import Destroy
from ontology.interop.System.Storage import GetContext

def Main(operation, args):
    if operation == 'getStorageContext':
        return getStorageContext()
    if operation == 'destroy':
        return destroy()
    return False

def getStorageContext():
    context = GetContext()
    Hash = GetExecutingScriptHash()
    contract = GetContract(Hash)
    context1 = GetStorageContext(contract)
    Notify(context1)
    Notify(context)
    return True

def destroy():
    Destroy()
    return True
