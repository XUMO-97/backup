from ontology.interop.Ontology.Contract import Migrate,GetScript
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.ExecutionEngine	import GetExecutingScriptHash
from ontology.interop.System.Blockchain import GetContract



def Main(operation, args):
    if operation == "MigrateContract":
        return MigrateContract(args[0])
    if operation == 'getScript':
        return getScript()
    return False

def MigrateContract(code):
    res = Migrate(code, "1", "1", "1", "1", "1", "1")
    res1 = res
    if res:
        return "Migrate successfully"
    else:
        return False

def getScript():
    script = GetExecutingScriptHash()
    contract = GetContract(script)
    sc = GetScript(contract)
    Notify(sc)
    return sc
