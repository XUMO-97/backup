from boa.interop.System.Blockchain import GetHeight, GetHeader, GetBlock, GetTransactionHeight, GetContract, GetTransactionByHash
from boa.interop.System.Block import GetTransactions, GetTransactionCount, GetTransactionByIndex
from boa.interop.System.Runtime import Notify

def Main(operation):
    if operation == 'demo':
        return demo()

    return False


def demo():
    block1=GetBlock(1408)
    res1=GetTransactionCount(block1)
    # block_hash="e40315e22fc30b4648e3546d33927317f7175dc4c866ea443077798240c5e016"
    block_hash=bytearray([228, 3, 21, 226, 47, 195, 11, 70, 72, 227, 84, 109, 51, 146, 115, 23, 247, 23, 93, 196, 200, 102, 234, 68, 48, 119, 121, 130, 64, 197, 224, 22])
    block2=GetBlock(block_hash)
    res2=GetTransactionCount(block2)
    return res1
