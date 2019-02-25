from ontology.interop.System.Block import GetTransactionCount,GetTransactions,GetTransaction
from ontology.interop.System.Storage	import Put,GetContext
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.interop.System.Blockchain import GetBlock
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.interop.System.Block	import GetTransactionByIndex

context = GetContext()

def Main(operation, args):
    if operation == 'getTransactionCount':
        return getTransactionCount()
    if operation == 'getTransactions':
        return getTransactions()
    return False

def getTransactionCount():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    Count = GetTransactionCount(Block)
    Put(context, "get", Count)
    return True

def getTransactions():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    txs = GetTransactions(Block)
    Hash = GetTransactionHash(txs[0])
    tx = GetTransactionByIndex(Block, 0)
    Hash1 = GetTransactionHash(tx)
    Put(context, "getHash", Hash)
    Put(context, "getHash1", Hash1)
    return True