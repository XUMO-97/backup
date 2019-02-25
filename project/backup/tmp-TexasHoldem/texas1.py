"""
TexasHoldem Game
"""
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash, Base58ToAddress
from ontology.builtins import concat, state, sha256
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.interop.System.App import DynamicAppCall

"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/Utils.py
"""


def RequireScriptHash(key):
    """
    Checks the bytearray parameter is script hash or not. Script Hash
    length should be equal to 20.
    :param key: bytearray parameter to check script hash format.
    :return: True if script hash or revert the transaction.
    """
    assert (len(key) == 20)
    return True


def RequireWitness(witness):
    """
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
    assert (CheckWitness(witness))
    return True


"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeMath.py
"""


def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    assert (c >= a)
    return c


def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    assert (a >= b)
    return a - b


def ASub(a, b):
    if a > b:
        return a - b
    if a < b:
        return b - a
    else:
        return 0


def Mul(a, b):
    """
    Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    if a == 0:
        return 0
    c = a * b
    assert (c / a == b)
    return c


def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    assert (b > 0)
    c = a / b
    return c


def Pwr(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c


def Sqrt(a):
    """
    Return sqrt of a
    :param a:
    :return: sqrt(a)
    """
    c = Div(Add(a, 1), 2)
    b = a
    while (c < b):
        b = c
        c = Div(Add(Div(a, c), c), 2)
    return c


ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
LUCKY_CONTRACT_HASH_KEY = "LuckyContract"
CHIP_CONTRACT_HASH_KEY = "ChipContract"
Admin = Base58ToAddress('ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS')
INIT_KEY = "Inited"

PLAYER_LAST_CHECK_IN_DAY = "P11111"
PLAYER_UID_PRE_KEY = "P2222"
PROJECT_ID_PRE_KEY = "P3"
POKE_HASH_PRE_KEY = "P4"
PLAYER_HAND_POKE_KEY = "P5"
PLAYER_REFERRAL_KEY = "P6"

COMMON_POKE_KEY = "C1"
CHIP_TO_ONG_RATE_KEY = "C2"

GAME_STATUS_KEY = "G1"
GAME_PLAYER_LIST_KEY = "G2"
GAME_WINNER_KEY = "G3"
GAME_KEYVALUE_LIST_KEY = "G4"
GAME_SALT_KEY = "G5"

TOTAL_ONG_FOR_ADMIN = "T1111111"
TOTAL_LUCKY_FOR_ADMIN = "T2"
TOTAL_CHIP_FOR_ADMIN = "T3"

LUCKY_TO_ONG_RATE_KEY = "L1"

REFERRAL_BONUS_PERCENTAGE_KEY = "R6"

ONG_BALANCE_KEY = "O1"

ONGMagnitude = 1000000000
LuckyDecimals = 9
LuckyMagnitude = 1000000000
ChipDecimals = 9
ChipMagnitude = 1000000000
Magnitude = 1000000000000000000000000000000
DaySeconds = 86400
CheckInRewardChipNum = 1000
ContractAddress = GetExecutingScriptHash()


def Main(operation, args):
    if operation == "init":
        return init()
    if operation == "checkIn":
        assert (len(args) == 2)
        player = args[0]
        uid = args[1]
        return checkIn(player, uid)
    if operation == "canCheckIn":
        assert (len(args) == 1)
        account = args[0]
        return canCheckIn(account)

    if operation == "startGame":
        assert (len(args) == 3)
        pokeHashList = args[0]
        playerList = args[1]
        gameId = args[2]
        return startGame(pokeHashList, playerList, gameId)
    if operation == "getCommonPoke":
        assert (len(args) == 1)
        gameId = args[0]
        return getCommonPoke(gameId)
    if operation == "playerGetHandPoke":
        assert (len(args) == 2)
        gameId = args[0]
        player = args[1]
        return playerGetHandPoke(gameId, player)
    if operation == "endGame":
        assert (len(args) == 3)
        gameId = args[0]
        winner = args[1]
        salt = args[2]
        return endGame(gameId, winner, salt)
    if operation == "getSaltAfterEnd":
        assert (len(args) == 1)
        gameId = args[0]
        return getSaltAfterEnd(gameId)
    if operation == "checkPokeHash":
        assert (len(args) == 2)
        gameId = args[0]
        pokeNum = args[1]
        return checkPokeHash(gameId, pokeNum)
    if operation == "migrateContract":
        assert (len(args) == 7)
        code = args[0]
        needStorage = args[1]
        name = args[2]
        version = args[3]
        author = args[4]
        email = args[5]
        description = args[6]
        return migrateContract(code, needStorage, name, version, author, email, description)
    if operation == "getPokeHashList":
        pokeNum = args[0]
        salt = args[1]
        return getPokeHashList(pokeNum, salt)


def init():
    """
    only admin can init.
    :return: bool
    """
    RequireWitness(Admin)
    inited = Get(GetContext(), INIT_KEY)
    if inited:
        Notify(["Idiot admin, you have initialized the contract"])
        return False
    else:
        Put(GetContext(), INIT_KEY, 1)

        Notify(["Initialized contract successfully"])
    return True


def setLuckyContractHash(reversedLuckyContractHash):
    RequireWitness(Admin)
    Put(GetContext(), LUCKY_CONTRACT_HASH_KEY, reversedLuckyContractHash)
    Notify(["setLuckyContractHash", reversedLuckyContractHash])
    return True


def setChipContractHash(reversedChipContractHash):
    RequireWitness(Admin)
    Put(GetContext(), CHIP_CONTRACT_HASH_KEY, reversedChipContractHash)
    Notify(["setLuckyContractHash", reversedChipContractHash])
    return True


def setChipToOngRate(ong, chip):
    RequireWitness(Admin)
    Put(GetContext(), CHIP_TO_ONG_RATE_KEY, Div(Mul(Mul(chip, ChipMagnitude), Magnitude), Mul(ong, ONGMagnitude)))
    Notify(["setRate", ong, chip])
    return True


# def setLuckyToOngRate(ong, lucky):
#     RequireWitness(Admin)
#     Put(GetContext(), LUCKY_TO_ONG_RATE_KEY, Div(Mul(Mul(lucky, LuckyMagnitude), Magnitude), Mul(ong, ONGMagnitude)))
#     Notify(["setRate", ong, lucky])
#     return True


def checkIn(player, uid):
    """
    check in function
    :param account: player's account addresss
    :param uid: player's uid
    :return: bool
    """
    RequireWitness(player)
    # check uid legality

    # checkUid = Get(GetContext(), concatKey(PLAYER_UID_PRE_KEY, player))
    # if not checkUid:
    #     Put(GetContext(), concatKey(PLAYER_UID_PRE_KEY, player), uid)
    # else:
    #     assert(checkUid == uid)

    checkInDays = canCheckIn(player)
    assert (checkInDays)
    Put(GetContext(), concatKey(PLAYER_LAST_CHECK_IN_DAY, player), checkInDays)

    Notify(["checkIn", player, uid, checkInDays])
    return True


def canCheckIn(player):
    """
    :param account: player's account address
    :return: return == 0 => can NOT check in.
              return > 0 => can check in.
    """
    lastTimeCheckIn = Get(GetContext(), concatKey(PLAYER_LAST_CHECK_IN_DAY, player))
    # now = GetTime()
    now = Add(GetTime(), Mul(8, 3600))
    days = Div(now, DaySeconds)
    if not lastTimeCheckIn:
        return days

    if days > lastTimeCheckIn:
        return days
    else:
        return 0


def projectReward(rewardList):
    RequireWitness(Admin)
    account = rewardList[0]
    uid = rewardList[1]
    projectId = rewardList[2]

    checkUid = Get(GetContext(), concatKey(PLAYER_UID_PRE_KEY, account))
    assert (uid == checkUid)

    completeProjectList = Get(GetContext(), concatKey(PROJECT_ID_PRE_KEY, account))
    if not completeProjectList:
        completeProjectList = []
    else:
        completeProjectList = Deserialize(completeProjectList)

    completeProjectList.append(projectId)
    Put(GetContext(), concatKey(PROJECT_ID_PRE_KEY, account), Serialize(completeProjectList))
    Notify(["getReward", account, uid, projectId])
    return True


def startGame(pokeHashListBase, playerList, gameId):
    RequireWitness(Admin)
    playerNum = len(playerList)
    pokeNum = len(pokeHashListBase)
    pokeHashInHand = []
    pokeHashList = pokeHashListBase
    tmp = 0
    helperRandom = abs(GetCurrentBlockHash()) % pokeNum
    playersPokersList = []
    while tmp < playerNum:
        playerPokeList = []
        poker1 = pokeHashListBase[helperRandom]
        pokeHashListBase.remove(helperRandom)
        playerPokeList.append(poker1)
        pokeNum = pokeNum - 1

        helperRandom = abs(sha256(concat(helperRandom, poker1))) % pokeNum
        poker2 = pokeHashListBase[helperRandom]
        pokeHashListBase.remove(helperRandom)
        playerPokeList.append(poker2)
        pokeNum = pokeNum - 1

        helperRandom = abs(sha256(concat(helperRandom, poker2))) % pokeNum

        playersPokersList.append(playerPokeList)

        tmp = tmp + 1

    commonPokeList = []
    commonPokeNum = 0
    while commonPokeNum < 5:
        poker = pokeHashListBase[helperRandom]
        pokeHashListBase.remove(helperRandom)
        commonPokeList.append(poker)
        pokeNum = pokeNum - 1

        helperRandom = abs(sha256(concat(helperRandom, poker))) % pokeNum

        commonPokeNum += 1

    Notify(["startGame", pokeHashListBase, commonPokeList, playersPokersList, gameId])
    return commonPokeList


def getCommonPoke(gameId):
    commonPokeList = Get(GetContext(), concatKey(gameId, COMMON_POKE_KEY))
    commonPokeList = Deserialize(commonPokeList)
    Notify(["commonPoke", gameId, commonPokeList])
    return commonPokeList


def playerGetHandPoke(gameId, player):
    RequireWitness(player)
    handPokeList = Get(GetContext(), concatKey(gameId, concatKey(player, PLAYER_HAND_POKE_KEY)))
    handPokeList = Deserialize(handPokeList)

    Notify(["playerHandPoke", gameId, player, handPokeList])
    return handPokeList


def endGame(gameId, winner, salt):
    RequireScriptHash(winner)

    # check and set game status
    gameStatus = Get(GetContext(), concatKey(gameId, GAME_STATUS_KEY))
    assert (gameStatus == 1)
    gameStatus = 2
    Put(GetContext(), concatKey(gameId, GAME_STATUS_KEY), gameStatus)

    # check winner in player list and set winner
    playerList = Get(GetContext(), concatKey(gameId, GAME_PLAYER_LIST_KEY))
    playerList = Deserialize(playerList)
    checkWinner = False
    for player in playerList:
        if player == winner:
            Put(GetContext(), concatKey(gameId, GAME_WINNER_KEY), winner)
            checkWinner = True
    assert (checkWinner)

    # set salt
    Put(GetContext(), concatKey(gameId, GAME_SALT_KEY), salt)

    Notify(["endGame", gameId, winner, salt])
    return True


def adminInvest(ongAmount, luckyAmount, ChipAmount):
    RequireWitness(Admin)
    assert (_transferONG(Admin, ContractAddress, ongAmount))
    Put(GetContext(), TOTAL_ONG_FOR_ADMIN, Add(getTotalOngForAdmin(), ongAmount))

    assert (_transferLucky(Admin, ContractAddress, ongAmount))
    Put(GetContext(), TOTAL_LUCKY_FOR_ADMIN, Add(getTotalOngForAdmin(), ongAmount))

    assert (_transferChip(Admin, ContractAddress, ongAmount))
    Put(GetContext(), TOTAL_CHIP_FOR_ADMIN, Add(getTotalOngForAdmin(), ongAmount))

    Notify(["adminInvest", ongAmount])
    return True


def getSaltAfterEnd(gameId):
    salt = Get(GetContext(), concatKey(gameId, GAME_SALT_KEY))
    Notify([salt])
    return salt


def checkPokeHash(gameId, pokeNum):
    assert (pokeNum >= 1)
    assert (pokeNum <= 52)
    salt = getSaltAfterEnd(gameId)
    pokeHash = sha256(pokeNum) ^ sha256(salt)
    Notify([pokeHash])
    return pokeHash


def setReferralBonusPercentage(referralBonus):
    RequireWitness(Admin)
    assert (referralBonus >= 0)
    assert (referralBonus <= 100)
    Put(GetContext(), REFERRAL_BONUS_PERCENTAGE_KEY, referralBonus)
    Notify(["setReferralBonus", referralBonus])
    return True


def addReferral(toBeReferred, referral):
    RequireWitness(Admin)
    RequireScriptHash(toBeReferred)
    RequireScriptHash(referral)
    assert (not getReferral(toBeReferred))
    assert (toBeReferred != referral)
    Put(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred), referral)
    Notify(["addReferral", toBeReferred, referral])
    return True


def addMultiReferral(toBeReferredReferralList):
    RequireWitness(Admin)
    for toBeReferredReferral in toBeReferredReferralList:
        toBeReferred = toBeReferredReferral[0]
        referral = toBeReferredReferral[1]
        RequireScriptHash(toBeReferred)
        RequireScriptHash(referral)
        assert (not getReferral(toBeReferred))
        assert (toBeReferred != referral)
        Put(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred), referral)
    Notify(["addMultiReferral", toBeReferredReferralList])
    return True


def getLuckyToOngRate():
    """
    Div(Mul(Mul(lucky, LuckyMagnitude), Magnitude), Mul(ong, ONGMagnitude))
     lucky * 10^9
    ------------- * Magnitude
     ong * 10^9
    :return:
    """
    return Get(GetContext(), LUCKY_TO_ONG_RATE_KEY)


def getReferralBonusPercentage():
    return Get(GetContext(), REFERRAL_BONUS_PERCENTAGE_KEY)


def withdraw(account):
    RequireWitness(account)
    ongAmountToBeWithdraw = getOngBalanceOf(account)
    assert (ongAmountToBeWithdraw > 0)
    assert (_transferONGFromContract(account, ongAmountToBeWithdraw))
    Delete(GetContext(), concatKey(ONG_BALANCE_KEY, account))
    Notify(["withdraw", account, ongAmountToBeWithdraw])
    return True


def getOngBalanceOf(account):
    return Get(GetContext(), concatKey(ONG_BALANCE_KEY, account))


def getTotalOngForAdmin():
    return Get(GetContext(), TOTAL_ONG_FOR_ADMIN)


def _transferONGFromContract(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        Notify(["transferOng", toAcct, amount])
        return True
    else:
        return False


def _transferONG(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        Notify(["transferOng", fromAcct, toAcct, amount])
        return True
    else:
        return False


def _tranferChipFromContract(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    chipContractAddress = Get(GetContext(), CHIP_CONTRACT_HASH_KEY)
    res = DynamicAppCall(chipContractAddress, "transfer", param)
    assert (res)
    Notify(["transferChip", toAcct, amount])
    return True


def _transferChip(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(fromAcct, toAcct, amount)
    chipContractAddress = Get(GetContext(), CHIP_CONTRACT_HASH_KEY)
    res = DynamicAppCall(chipContractAddress, "transfer", param)
    assert (res)
    Notify(["transferChip", fromAcct, toAcct, amount])
    return True


def _tranferLuckyFromContract(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    luckyContractAddress = Get(GetContext(), LUCKY_CONTRACT_HASH_KEY)
    res = DynamicAppCall(luckyContractAddress, "transfer", param)
    assert (res)
    Notify(["transferLucky", toAcct, amount])
    return True


def _transferLucky(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(ContractAddress, toAcct, amount)
    luckyContractAddress = Get(GetContext(), LUCKY_CONTRACT_HASH_KEY)
    res = DynamicAppCall(luckyContractAddress, "transfer", param)
    assert (res)
    Notify(["transferLucky", fromAcct, toAcct, amount])
    return True


def migrateContract(code, needStorage, name, version, author, email, description):
    RequireWitness(Admin)
    res = Migrate(code, needStorage, name, version, author, email, description)
    assert (res)
    Notify(["Migrate Contract successfully"])
    return True


def getReferral(toBeReferred):
    return Get(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred))


def concatKey(str1, str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)


def getPokeHashList(pokeNum, salt):
    pokeHashList = Get(GetContext(), POKE_HASH_PRE_KEY)
    if not pokeHashList:
        pokeHashList = []
    else:
        pokeHashList = Deserialize(pokeHashList)
    pokeHash = sha256(pokeNum) ^ sha256(salt)
    pokeHashList.append(pokeHash)
    Put(GetContext(), POKE_HASH_PRE_KEY, Serialize(pokeHashList))
    Notify([pokeHashList])
    return pokeHashList
