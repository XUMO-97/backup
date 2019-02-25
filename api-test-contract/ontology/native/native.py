from ontology.interop.Ontology.Native import Invoke
from ontology.builtins import ToScriptHash, state
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.Ontology.Runtime	import Base58ToAddress

# ONG Big endian Script Hash: 0x0200000000000000000000000000000000000000
OngContract = Base58ToAddress("AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ")
fromAccount = Base58ToAddress("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS")


selfContractAddress = GetExecutingScriptHash()

def Main(operation, args):
    if operation == "transferOngToContract":
        return transferOngToContract()
    if operation == "checkSelfContractONGAmount":
        return checkSelfContractONGAmount()
    return False

def transferOngToContract():
    Notify(["111_transferOngToContract", selfContractAddress])
    param = state(fromAccount, selfContractAddress, 1)
    res = Invoke(0, OngContract, 'transfer', [param])
    if res and res == b'\x01':
        Notify('transfer Ong succeed')
        return True
    else:
        Notify('transfer Ong failed')
        return False

def checkSelfContractONGAmount():
    param = state(selfContractAddress)
    # do not use [param]
    res = Invoke(0, OngContract, 'balanceOf', param)
    Notify(res)
    return res
