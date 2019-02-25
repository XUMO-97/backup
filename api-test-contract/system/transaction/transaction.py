from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Transaction	import GetTransactionHash
from ontology.interop.System.Blockchain import GetHeight,GetBlock,GetTransactionHeight
from ontology.interop.System.Block import GetTransactionByIndex
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash

def Main(operation, args):
    if operation == 'getHash':
        return getHash()
    return False

def getHash():
    Hash = GetCurrentBlockHash()
    Block = GetBlock(Hash)
    tx = GetTransactionByIndex(Block, 0)
    Hash = GetTransactionHash(tx)
    Notify(Hash)
    return True