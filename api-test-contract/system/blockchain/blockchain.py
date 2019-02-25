from ontology.interop.System.Blockchain import GetHeight,GetHeader,GetBlock,GetTransactionByHash,GetContract,GetTransactionHeight
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.interop.System.Storage import Put
from ontology.interop.System.Storage import GetContext
from ontology.interop.System.Runtime	import Notify
from ontology.interop.System.Header import GetBlockHash
from ontology.interop.System.Block import GetTransactionCount,GetTransactionByIndex
from ontology.interop.System.ExecutionEngine	import GetExecutingScriptHash,GetCallingScriptHash,GetEntryScriptHash
from ontology.interop.Ontology.Contract import GetScript
from ontology.interop.System.Transaction	import GetTransactionHash

context = GetContext()

def Main(operation, args):
    if operation == 'getHeight':
        return getHeight()
    if operation == 'getHeader':
        return getHeader()
    if operation == 'getBlock':
        return getBlock()
    if operation == 'getTransaction':
        return getTransaction()
    if operation == 'getContract':
        return getContract()
    if operation == 'getTransactionHeight':
        return getTransactionHeight()
    return False

def getHeight():
    height = GetHeight()
    Put(context, "get", height)
    Notify(height)
    return True

def getHeader():
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    HashFromHeader = GetBlockHash(header)
    Put(context, "gethash", Hash)
    Put(context, "gethashfromheader", HashFromHeader)
    return True

def getBlock():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    Count = GetTransactionCount(Block)
    Put(context, "get", Count)
    return True

def getTransaction():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    tx = GetTransactionByIndex(Block, 0)
    h = GetTransactionHash(tx)
    t = GetTransactionByHash(h)
    h1 = GetTransactionHash(t)
    Put(context, "getHash", h)
    Put(context, "getHash1", h1)
    return True

def getContract():
    Hash = GetExecutingScriptHash()
    contract = GetContract(Hash)
    script = GetScript(contract)
    Put(context, "get", script)
    return True

def getTransactionHeight():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    tx = GetTransactionByIndex(Block, 0)
    txh = GetTransactionHash(tx)
    height = GetTransactionHeight(txh)
    Put(context, "get", height)
    return True