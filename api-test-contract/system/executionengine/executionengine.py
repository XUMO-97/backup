from ontology.interop.System.ExecutionEngine import GetScriptContainer,GetExecutingScriptHash,GetCallingScriptHash,GetEntryScriptHash
from ontology.interop.System.Transaction	import GetTransactionHash
from ontology.interop.System.Storage	import Put
from ontology.interop.System.Storage	import GetContext
from ontology.interop.System.Runtime	import Notify
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.interop.System.Blockchain import GetBlock
from ontology.interop.System.Block import GetTransactionByIndex
from ontology.interop.Ontology.Contract import GetScript

context = GetContext()

def Main(operation, args):
    if operation == 'getScriptContainer':
        return getScriptContainer()
    if operation == 'getExecutingScriptHash':
        return getExecutingScriptHash()
    if operation == 'getCallingScriptHash':
        return getCallingScriptHash()
    return False

def getScriptContainer():
    container = GetScriptContainer()
    Hash = GetTransactionHash(container)
    bhash = GetCurrentBlockHash()
    block = GetBlock(bhash)
    tx = GetTransactionByIndex(block, 0)
    tHash = GetTransactionHash(tx)
    Put(context, 'get', Hash)
    Put(context, 'get1', tHash)
    return True

def getExecutingScriptHash():
    Hash = GetExecutingScriptHash()
    Put(context, 'get', Hash)
    Notify(Hash)
    return True

def getCallingScriptHash():
    Hash = GetCallingScriptHash()
    Hash1 = GetEntryScriptHash()
    Notify(Hash)
    Notify(Hash1)
    return True