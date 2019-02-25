OntCversion = '2.0.0'
"""
Registry Smart Contract
"""
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, state, sha256, has_key, remove
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.libont import str, int

SelfContractHash = GetExecutingScriptHash()



TOKEN_CONTRACT_REVERSED_HASH = "ContractHash"
PLCR_CONTRACT_REVERSED_HASH = "PLCRContractHash"
PARAMETERIZER_CONTRACT_REVERSED_HASH = "ParamContractHash"

NAME_KEY = "Name1"

# LISTING_MAP_KEY + listingHash --- store the listingHash data
LISTING_MAP_KEY = "ListMap"

# CHALLENGE_MAP_KEY + pollID ---  store associated challenge data except tokenClaims
CHALLENGE_MAP_KEY = "Challenge"
# CHALLENGE_TOKEN_CLAIMS_KEY + pollID + address --- store
CHALLENGE_TOKEN_CLAIMS_KEY = "C1"




def Main(operation, args):
    if operation == "init":
        if len(args) != 4:
            return False
        tokenRCH = args[0]
        plcrRCH = args[1]
        paramRCH = args[2]
        name = args[3]
        return init(tokenRCH, plcrRCH, paramRCH, name)
    if operation == "apply":
        if len(args) != 4:
            return False
        account = args[0]
        listingHash = args[1]
        amount = args[2]
        data = args[3]
        return apply(account, listingHash, amount, data)
    if operation == "deposit":
        if len(args) != 3:
            return False
        account = args[0]
        listingHash = args[1]
        amount = args[2]
        return deposit(account, listingHash, amount)
    if operation == "withdraw":
        if len(args) != 3:
            return False
        account = args[0]
        listingHash = args[1]
        amount = args[2]
        return withdraw(account, listingHash, amount)
    if operation == "exit":
        if len(args) != 2:
            return False
        account = args[0]
        listingHash = args[1]
        return exit(account, listingHash)
    if operation == "challenge":
        if len(args) != 3:
            return False
        account = args[0]
        listingHash = args[1]
        data = args[2]
        return challenge(account, listingHash, data)
    if operation == "updateStatus":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return updateStatus(listingHash)
    if operation == "updateStatuses":
        if len(args) != 1:
            return False
        listingHashList = args[0]
        return updateStatuses(listingHashList)
    if operation == "claimReward":
        if len(args) != 2:
            return False
        account = args[0]
        challengeID = args[1]
        return claimReward(account, challengeID)
    if operation == "claimRewards":
        if len(args) != 2:
            return False
        accountList = args[0]
        challengeIDList = args[1]
        return claimRewards(accountList, challengeIDList)
    if operation == "voterReward":
        if len(args) != 2:
            return False
        voter = args[0]
        challengeID = args[1]
        return voterReward(voter, challengeID)
    if operation == "canBeWhitelisted":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return canBeWhitelisted(listingHash)
    if operation == "isWhitelisted":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return isWhitelisted(listingHash)
    if operation == "getData":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return getData(listingHash)
    if operation == "appWasMade":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return appWasMade(listingHash)
    if operation == "challengeExists":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return challengeExists(listingHash)
    if operation == "challengeCanBeResolved":
        if len(args) != 1:
            return False
        listingHash = args[0]
        return challengeCanBeResolved(listingHash)
    if operation == "determineReward":
        if len(args) != 1:
            return False
        challengeID = args[0]
        return determineReward(challengeID)
    if operation == "tokenClaims":
        if len(args) != 2:
            return False
        challengeID = args[0]
        voter = args[1]
        return tokenClaims(challengeID, voter)
    if operation == "barrier":
        if len(args) != 3:
            return False
        listingHash = args[0]
        helperSalt = args[1]
        mode = args[2]
        return barrier(listingHash, helperSalt, mode)
    if operation == "getTokenRCH":
        return getTokenRCH()
    if operation == "getPLCRRCH":
        return getPLCRRCH()
    if operation == "getParamRCH":
        return getParamRCH()
    return False


def init(tokenRCH, plcrRCH, paramRCH, name):
    assert(not getTokenRCH() and len(tokenRCH) == 20)
    assert(not getPLCRRCH() and len(plcrRCH) == 20)
    assert(not getParamRCH() and len(paramRCH) == 20)
    Put(GetContext(), TOKEN_CONTRACT_REVERSED_HASH, tokenRCH)
    Put(GetContext(), PLCR_CONTRACT_REVERSED_HASH, plcrRCH)
    Put(GetContext(), PARAMETERIZER_CONTRACT_REVERSED_HASH, paramRCH)
    Put(GetContext(), NAME_KEY, name)
    return True


def apply(account, listingHash, amount, data):
    assert(CheckWitness(account))
    assert(not isWhitelisted(listingHash))
    assert(not appWasMade(listingHash))
    paramHash = getParamRCH()
    params = ["minDeposit"]
    minDeposit = DynamicAppCall(paramHash, "get", params)
    Notify(["555", minDeposit])
    assert(amount >= minDeposit)

    applyStageLen = DynamicAppCall(paramHash, "get", ["applyStageLen"])
    # set owner, applyStageLen, endTime and data
    listing = {
        "owner": account,
        "applyStageLen": applyStageLen,
        "applicationExpiry": Add(GetTime(), applyStageLen),
        "unstakedDeposit": amount,
        "data": data,
        "whitelisted":False,
        "challengeID": 0
    }
    Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))

    # transfer tokens from account to Registry contract
    res = DynamicAppCall(getTokenRCH(), "transfer", [account, SelfContractHash, amount])
    assert(res)

    Notify(["application", listingHash, amount, listing["applyStageLen"], listing["applicationExpiry"], data, account])
    return True


def deposit(account, listingHash, amount):
    assert(CheckWitness(account))
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    assert(listing["owner"] == account)

    res = DynamicAppCall(getTokenRCH(), "transfer", [account, SelfContractHash, amount])
    assert(res)
    listing["unstakedDeposit"] = Add(listing["unstakedDeposit"], amount)
    Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))

    Notify(["deposit", listingHash, amount, listing["unstakedDeposit"], account])
    return True


def withdraw(account, listingHash, amount):
    assert(CheckWitness(account))
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)

    assert(listing["owner"] == account)
    assert(amount <= listing["unstakedDeposit"])

    minDeposit = DynamicAppCall(getParamRCH(), "get", ["minDeposit"])
    unstakeDepositLeft = Sub(listing["unstakedDeposit"], amount)
    assert( unstakeDepositLeft>= minDeposit)

    res = DynamicAppCall(getTokenRCH(), "transfer", [SelfContractHash, account, amount])
    assert(res)
    listing["unstakedDeposit"] = unstakeDepositLeft
    Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))
    Notify(["withdraw", listingHash, amount, listing["unstakedDeposit"], account])
    return True

def exit(account, listingHash):
    assert(CheckWitness(account))
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)

    assert(listing["owner"] == account)
    assert(isWhitelisted(listingHash))

    # cannot exit during ongoing challenge
    challengeID = listing["challengeID"]
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    assert(challengeID == 0 or challenge["resolved"])

    # remove listingHash and return tokens
    _resetListing(listingHash)

    Notify(["listingWithdrawn", listingHash])
    return True


def challenge(account, listingHash, data):
    assert(CheckWitness(account))
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    minDeposit = DynamicAppCall(getParamRCH(), "get", ["minDeposit"])
    Notify(["555", minDeposit])

    # listing must be in apply stage or already on the whitelist
    assert(appWasMade(listingHash) or listing["whitelisted"])

    # prevent multiple challenges
    challengeID = listing["challengeID"]


    if challengeID != 0:
        challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
        challenge = Deserialize(challengeInfo)
        assert(challenge["resolved"])
    # assert(challengeID == 0 or challenge["resolved"])


    # to prevent mass challenges when an application was just made, which result
    # in wasting gas, we create a moving barrier where the number of addresses
    # allowed to challenge increases over time.
    # if not listing["whitelisted"]:
    #     applyStageLen = listing["applyStageLen"]
    #     assert(GetTime() > Add(Sub(listing["applicationExpiry"], applyStageLen), barrier(listingHash, account, applyStageLen)))

    if listing["unstakedDeposit"] < minDeposit:
        # not enough tokens, listingHash auto-delisted
        _resetListing(listingHash)
        Notify(["touchAndRemove", listingHash])
        return 0

    # start poll
    voteQuorum = DynamicAppCall(getParamRCH(), "get", ["voteQuorum"])
    commitStageLen = DynamicAppCall(getParamRCH(), "get", ["commitStageLen"])
    revealStageLen = DynamicAppCall(getParamRCH(), "get", ["revealStageLen"])
    pollID = DynamicAppCall(getPLCRRCH(), "startPoll", [voteQuorum, commitStageLen, revealStageLen])

    dispenssationPct = DynamicAppCall(getParamRCH(), "get", ["dispensationPct"])
    challenge = {
        "challenger": account,
        "rewardPool":Div(Mul(Sub(100, dispenssationPct), minDeposit), 100),
        "stake": minDeposit,
        "resolved": False,
        "totalTokens": 0
    }
    Put(GetContext(), _concatKey(CHALLENGE_MAP_KEY, pollID), Serialize(challenge))

    # update listingHash to store most recent challenge
    listing["challengeID"] = pollID

    # lock tokens for listingHash during challenge
    listing["unstakedDeposit"] = Sub(listing["unstakedDeposit"], minDeposit)
    Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))

    # take tokens from challenger
    res = DynamicAppCall(getTokenRCH(), "transfer", [account, SelfContractHash, minDeposit])
    assert(res)

    endTimeList = DynamicAppCall(getPLCRRCH(), "getEndTimeList", [pollID])
    commitEndTime = endTimeList[0]
    revealEndTime = endTimeList[1]

    Notify(["challenge", listingHash, pollID, data, commitEndTime, revealEndTime, account])
    return pollID


def updateStatus(listingHash):
    if canBeWhitelisted(listingHash):
        assert(_whitelistApplication(listingHash))
    elif challengeCanBeResolved(listingHash):
        _resolveChallenge(listingHash)
    else:
        raise Exception("rollBack!")
    return True


def updateStatuses(listingHashList):
    for listingHash in listingHashList:
        assert(updateStatus(listingHash))
    return True


def claimReward(account, challengeID):
    # ensure the voter has not already claimied token and challenge results have been processed
    claimed = Get(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), account))
    assert(claimed == False)

    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    assert(challenge["resolved"] == True)

    voterTokens = DynamicAppCall(getPLCRRCH(), "getNumPassingTokens", [account, challengeID])
    reward = voterReward(account, challengeID)

    # subtract the voter's information to preserve the participant ratios of other voters
    # compared to the remaining pool of rewards
    challenge["totalTokens"] = Sub(challenge["totalTokens"], voterTokens)
    challenge["rewardPool"] = Sub(challenge["rewardPool"], reward)

    Put(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID), Serialize(challenge))

    # ensure a voter cannot claim tokens again
    Put(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), account), True)

    res = DynamicAppCall(getTokenRCH(), "transfer", [SelfContractHash, account, reward])
    assert(res)
    Notify(["rewardClaimed", challengeID, reward, account])
    return True

def claimRewards(accountList, challengeIDList):
    listLen = len(accountList)
    assert(listLen == len(challengeIDList))
    index = 0
    while index < listLen:
        account = accountList[index]
        challengeID = challengeIDList[index]
        assert(claimReward(account, challengeID))
        index = Add(index, 1)
    return True



def voterReward(voter, challengeID):
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    totalTokens = challenge["totalTokens"]
    rewardPool = challenge["rewardPool"]
    voterTokens = DynamicAppCall(getPLCRRCH(), "getNumPassingTokens", [voter, challengeID])
    return Div(Mul(voterTokens, rewardPool), totalTokens)


def canBeWhitelisted(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    challengeID = listing["challengeID"]

    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)

    # ensure that the application was made, the application period has ended
    # the listingHash can be whitelisted, and either:
    # the challengeID == 0 or the challenge has been resolved
    appWasMadeF = appWasMade(listingHash)
    applicationEnded = listing["applicationExpiry"] < GetTime()
    ableToBeWhitelisted = not isWhitelisted(listingHash)
    IDisZeroOrResolved = challengeID == 0 or challenge["resolved"] == True

    return appWasMadeF and applicationEnded and ableToBeWhitelisted and IDisZeroOrResolved


def isWhitelisted(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    if listing.has_key("whitelisted"):
        return listing["whitelisted"]
    else:
        return False


def getData(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    if isWhitelisted(listingHash):
        return [True, listing["data"]]
    else:
        return [False, ""]


def appWasMade(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    if listing.has_key("applicationExpiry"):
        return listing["applicationExpiry"]
    else:
        return False


def challengeExists(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)

    challengeID = listing["challengeID"]

    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    return listing["challengeID"] > 0 and (not challenge["resolved"])


def challengeCanBeResolved(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)

    challengeID = listing["challengeID"]
    assert(challengeExists(listingHash))

    return DynamicAppCall(getPLCRRCH(), "pollEnded", [challengeID])


def determineReward(challengeID):
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    notResolved = not challenge["resolved"]
    votingEnded = DynamicAppCall(getPLCRRCH(), "pollEnded", [challengeID])
    assert(notResolved and votingEnded)

    stake = challenge["stake"]
    # edge case, nobody voted, give all tokens to the challenger
    totalNumberOfTokensForWinningOption = DynamicAppCall(getPLCRRCH(), "getTotalNumberOfTokensForWinningOption", [challengeID])
    if totalNumberOfTokensForWinningOption == 0:
        # edge case, nobody voted, give all tokens to the challenger
        return Mul(2, stake)

    rewardPool = challenge["rewardPoll"]
    return Sub(Mul(2, stake), rewardPool)




def tokenClaims(challengeID, voter):
    return Get(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), voter))

def barrier(listingHash, helperSalt, mode):
    assert(mode > 0 )
    return abs(sha256(_concatKey(sha256(listingHash), sha256(helperSalt)))) % mode

def getTokenRCH():
    return Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)

def getPLCRRCH():
    return Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)

def getParamRCH():
    return Get(GetContext(), PARAMETERIZER_CONTRACT_REVERSED_HASH)



def _resolveChallenge(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    challengeID = listing["challengeID"]

    # calculate the winner reward
    # which is (winner's full stake) + (dispensationPct * loser's stake)
    reward = determineReward(challengeID)

    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        # Error: 101, challengeID does not exist in Challenge Map
        Notify(["Error", 101])
        return False
    challenge = Deserialize(challengeInfo)
    # set falg on challenge being processed
    challenge["resolved"] = True

    # store the total tokens used for voting by the winning side for reward purposes
    plcrHash = getPLCRRCH()
    challenge["totalTokens"] = DynamicAppCall(plcrHash, "getTotalNumberOfTokensForWinningOption", [challengeID])

    Put(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID), Serialize(challenge))
    # case 1 : challenge failed
    isPassed = DynamicAppCall(plcrHash, "isPassed", [challengeID])

    if isPassed:
        assert(_whitelistApplication(listingHash))
        # unlock stake so that it can be retrieved by the applicant
        listing["unstakedDeposit"] = Add(listing["unstakedDeposit"], reward)
        Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))
        Notify(["challengeFailed", listingHash, challengeID, challenge["rewardPool"], challenge["totalTokens"]])
        return False
    # case 2 : challenge succeeded or nobody voted
    else:
        _resetListing(listingHash)
        # transfer the reward to the challenger
        res = DynamicAppCall(getTokenRCH(), "transfer", [SelfContractHash, challenge["challenger"], reward])
        assert(res)
        Notify(["challengeSucceeded", listingHash, challengeID, challenge["rewardPool"], challenge["totalTokens"]])
        return True




def _whitelistApplication(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    if not listing["whitelisted"]:
        Notify(["applicationWhitelisted", listingHash])
    listing["whitelisted"] = True
    Put(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash), Serialize(listing))
    return True


def _resetListing(listingHash):
    listingInfo = Get(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))
    if not listingInfo:
        return False
    listing = Deserialize(listingInfo)
    if listing["whitelisted"]:
        Notify(["listingRemoved", listingHash])
    else:
        Notify(["applicationRemoved", listingHash])

    # delete listing to prevent reentry
    owner = listing["owner"]
    unstakedDeposit = listing["unstakedDeposit"]
    Delete(GetContext(), _concatKey(LISTING_MAP_KEY, listingHash))

    # transfer any remaining balance back to the owner
    if unstakedDeposit > 0:
        res = DynamicAppCall(getTokenRCH(), "transfer", [SelfContractHash, owner, unstakedDeposit])
        assert(res)
    return True


def _concatKey(str1, str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)

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
	assert (a>=b)
	return a-b

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

