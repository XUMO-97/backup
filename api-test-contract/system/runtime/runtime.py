from ontology.interop.System.Runtime import Notify,Log,GetTrigger,CheckWitness,GetTime,Serialize,Deserialize
from ontology.interop.System.ExecutionEngine	import GetExecutingScriptHash
from ontology.interop.System.Blockchain import GetHeader
from ontology.interop.System.Header import GetTimestamp,GetBlockHash
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash  #,Log
from ontology.interop.System.Storage	import Put,GetContext

def Main(operation, args):
    if operation == 'getTrigger':
        return getTrigger()
    if operation == 'checkWitness':
        Hash = args[1]
        return checkWitness(Hash)
    # if operation == 'log':
    #     return log()
    if operation == 'notify':
        return notify()
    if operation == 'getTime':
        return getTime()
    if operation == 'serialize':
        return serialize()
    return False

def getTrigger():
    trigger = GetTrigger()
    Notify(trigger)
    return True

def checkWitness(Hash):
    check = CheckWitness(Hash)
    Notify(check)
    return True

# def log():
#     Log('aaaaa')
#     return True

def notify():
    Notify('aaaaa')
    return True

def getTime():
    time = GetTime()
    Hash = GetCurrentBlockHash()
    header = GetHeader(Hash)
    time1 = GetTimestamp(header)
    Notify(time)
    Notify(time1)
    return  True

def serialize():
    context = GetContext()
    time = GetTime()
    time1 = Serialize(time)
    time2 = Deserialize(time1)
    Notify(time)
    Notify(time2)
    return True
