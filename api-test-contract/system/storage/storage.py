from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Storage	import GetContext,GetReadOnlyContext,Get,Put,Delete
from ontology.interop.System.Contract import GetStorageContext
from ontology.interop.System.Blockchain import GetContract
from ontology.interop.System.ExecutionEngine	import GetExecutingScriptHash
from ontology.interop.System.StorageContext import AsReadOnly

def Main(operation, args):
    if operation == 'getContext':
        return getContext()
    if operation == 'put':
        return put()
    if operation == 'get':
        return get()
    if operation == 'delete':
        return delete()
    return False

context = GetContext()

def getContext():
    script = GetExecutingScriptHash()
    contract = GetContract(script)
    context1 = GetStorageContext(contract)
    Notify(context)
    Notify(context1)
    return True

def put():
    Put(context, 'get', 'aaaaa')
    return True

def get():
    Put(context, 'get', 'aaaaa')
    value = Get(context, 'get')
    Notify(value)
    return True

def delete():
    Put(context, 'get', 'aaaaa')
    Delete(context, 'get')
    value = Get(context, 'get')
    Notify(value)
    return True