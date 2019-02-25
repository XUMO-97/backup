from ontology.interop.System.Runtime import Notify
from ontology.interop.System.StorageContext import AsReadOnly
from ontology.interop.System.Storage import GetReadOnlyContext
from ontology.interop.System.Storage import GetContext
from ontology.interop.System.Storage	import Put,Get

context = GetContext()

def Main(operation, args):
    if operation == 'asReadOnly':
        return asReadOnly()
    if operation == 'put':
        return put()
    return False

def asReadOnly():
    newContext = AsReadOnly(context)
    context1 = GetReadOnlyContext()
    Notify(context)
    Notify(context1)
    Notify(newContext)
    return True

def put():
    context1 = GetReadOnlyContext()
    Put(context1, 'get', 'only')
    return True
