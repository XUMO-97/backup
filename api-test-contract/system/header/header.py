from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Header import GetIndex,GetBlockHash,GetPrevHash,GetTimestamp
from ontology.interop.System.Blockchain import GetHeight,GetHeader
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash

def Main(operation, args):
    if operation == 'getIndex':
        return getIndex()
    if operation == 'getHash':
        return getHash()
    if operation == 'getPrevHash':
        return getPrevHash()
    if operation == 'getTimestamp':
        return getTimestamp()
    return False

def getIndex():
    height = GetHeight()
    header = GetHeader(height)
    index = GetIndex(header)
    Notify(height)
    Notify(index)
    return True

def getHash():
    height = GetHeight()
    header = GetHeader(height)
    Hash = GetBlockHash(header)
    Notify(height)
    Notify(Hash)
    return True

def getPrevHash():
    height = GetHeight()
    header = GetHeader(height)
    preHash = GetPrevHash(header)
    Notify(height)
    Notify(preHash)
    return True

def getTimestamp():
    height = GetHeight()
    header = GetHeader(height)
    timestamp = GetTimestamp(header)
    Notify(height)
    Notify(timestamp)
    return True
