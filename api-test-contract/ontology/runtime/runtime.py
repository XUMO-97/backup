from ontology.interop.Ontology.Runtime import Base58ToAddress,AddressToBase58,GetCurrentBlockHash
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Storage	import Put,GetContext

context = GetContext()

def Main(operation, args):
    if operation == 'BTA':
        return BTA()
    if operation == 'ATB':
        return ATB()
    if operation == 'getHash':
        return getHash()
    return False

def BTA():
    bta = Base58ToAddress('ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS')
    return bta

def ATB():
    bta = BTA()
    atb = AddressToBase58(bta)
    return atb

def getHash():
    blockhash = GetCurrentBlockHash()
    Put(context, 'get', blockhash)
    return blockhash
