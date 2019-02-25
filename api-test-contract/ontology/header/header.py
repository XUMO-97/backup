from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Header import GetVersion,GetMerkleRoot,GetConsensusData,GetNextConsensus
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.interop.System.Blockchain import GetHeight,GetHeader

def Main(operation, args):
    if operation == 'getVersion':
        return getVersion()
    if operation == 'getMerkleRoot':
        return getMerkleRoot()
    if operation == 'getConsensusData':
        return getConsensusData()
    if operation == 'getNextConsensus':
        return getNextConsensus()
    return False

def getVersion():
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    version = GetVersion(header)
    return version

def getMerkleRoot():
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    merkleRoot = GetMerkleRoot(header)
    Notify(Hash)
    Notify(merkleRoot)
    return True

def getConsensusData():
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    ConsensusData = GetConsensusData(header)
    Notify(Hash)
    Notify(ConsensusData)
    return True

def getNextConsensus():
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    NextConsensus = GetNextConsensus(header)
    Notify(Hash)
    Notify(NextConsensus)
    return True
