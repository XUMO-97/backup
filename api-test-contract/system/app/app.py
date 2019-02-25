from ontology.interop.System.App	import RegisterAppCall
from ontology.interop.System.Runtime	import Notify
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash

OEP4Contract = RegisterAppCall('8cae506e0c37359626e341e44a2ab166055bec78', 'operation', 'args')
selfContractAddress = GetExecutingScriptHash()

def Main(operation, args):
    if operation == 'checkName':
        return checkName()
    return False

def checkName():
    # This "name" below should be consistent with your OEP4Contract methods
    # return OEP4Contract("name") is wrong
    # return OEP4Contract("name", []) or return OEP4Contract("name", 0) is correct!
    Notify(OEP4Contract("name", 0))
    return OEP4Contract("name", 0)