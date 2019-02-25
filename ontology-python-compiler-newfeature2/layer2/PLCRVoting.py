OntCversion = '2.0.0'
"""
PLCRVoting Smart Contract
"""
from ontology.interop.System.App import DynamicAppCall
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, sha256, has_key, remove
from ontology.libont import str, int

VOTE_TOKEN_BALANCE = "G1"
POLL_NOUNCE_KEY = "G2"
# DLL_MAP_KEY + address, --- DLL MAP DATA
DLL_MAP_KEY = "G3"

# Poll Info
# POLL_EXPIRE_KEY + pollID ,--- to store the expire date
POLL_COMMIT_END_KEY = "P1"
POLL_REVEAL_END_KEY = "P2"
POLL_VOTE_QUORUM_KEY = "P3"
POLL_VOTES_FOR_KEY = "P4"
POLL_VOTES_AGAINSt_KEY = "P5"
# POLL_DID_COMMIT_KEY + pollID + Account --- indicates whether an address committed a vote for this poll
POLL_DID_COMMIT_KEY = "P6"
# POLL_DID_REVEAL_KEY + pollID + Account --- indicates whether an address revealed a vote for this poll
POLL_DID_REVEAL_KEY = "P7"
# POLL_VOTE_OPTIONS_KEY + pollID + Account --- stores the voteOption of an address that revealed
POLL_VOTE_OPTIONS_KEY = "P8"


TOKEN_CONTRACT_REVERSED_HASH = "ContractHash"

Admin = Base58ToAddress("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS")

SelfContractHash = GetExecutingScriptHash()

def Main(operation, args):
    if operation == "init":
        if len(args) != 1:
            return False
        reversedTokenHash = args[0]
        return init(reversedTokenHash)
    if operation == "reSetTokenHash":
        if len(args) != 1:
            return False
        reversedTokenHash = args[0]
        return reSetTokenHash(reversedTokenHash)
    if operation == "requestVotingRights":
        if len(args) != 2:
            return False
        account = args[0]
        numTokens = args[1]
        return requestVotingRights(account, numTokens)
    if operation == "withdrawVotingRights":
        if len(args) != 2:
            return False
        account = args[0]
        numTokens = args[1]
        return withdrawVotingRights(account, numTokens)
    if operation == "rescueTokens":
        if len(args) != 2:
            return False
        voter = args[0]
        pollID = args[1]
        return rescueTokens(voter, pollID)
    if operation == "rescueTokensInMultiplePolls":
        if len(args) != 2:
            return False
        voterList = args[0]
        pollIDList = args[1]
        return rescueTokensInMultiplePolls(voterList, pollIDList)
    if operation == "getTokenHash":
        return getTokenHash()
    if operation == "getVoteTokenBalance":
        if len(args) != 1:
            return False
        account = args[0]
        return getVoteTokenBalance(account)
    if operation == "commitVote":
        if len(args) != 5:
            return False
        voter = args[0]
        pollID = args[1]
        secretHash = args[2]
        numTokens = args[3]
        prevPollID = args[4]
        return commitVote(voter, pollID, secretHash, numTokens, prevPollID)
    if operation == "commitVotes":
        if len(args) != 5:
            return False
        voterList = args[0]
        pollIDList = args[1]
        secretHashList = args[2]
        numTokensList = args[3]
        prevPollIDList = args[4]
        return commitVotes(voterList, pollIDList, secretHashList, numTokensList, prevPollIDList)
    if operation == "validPosition":
        if len(args) != 4:
            return False
        prevID = args[0]
        nextID = args[1]
        voter = args[2]
        numTokens = args[3]
        return validPosition(prevID, nextID, voter, numTokens)
    if operation == "revealVote":
        if len(args) != 4:
            return False
        voter = args[0]
        pollID = args[1]
        voteOption = args[2]
        salt = args[3]
        return revealVote(voter, pollID, voteOption, salt)
    if operation == "revealVotes":
        if len(args) != 4:
            return False
        voterList = args[0]
        pollIDList = args[1]
        voteOptionList = args[2]
        saltList = args[3]
        return revealVotes(voterList, pollIDList, voteOptionList, saltList)
    if operation == "getNumPassingTokens":
        if len(args) != 2:
            return False
        voter = args[0]
        pollID = args[1]
        return getNumPassingTokens(voter, pollID)
    if operation == "startPoll":
        if len(args) != 3:
            return False
        voteQuorum = args[0]
        commitDuration = args[1]
        revealDuration = args[2]
        return startPoll(voteQuorum, commitDuration, revealDuration)
    if operation == "isPassed":
        if len(args) != 1:
            return False
        pollID = args[0]
        return isPassed(pollID)
    if operation == "getTotalNumberOfTokensForWinningOption":
        if len(args) != 1:
            return False
        pollID = args[0]
        return getTotalNumberOfTokensForWinningOption(pollID)
    if operation == "pollEnded":
        if len(args) != 1:
            return False
        pollID = args[0]
        return pollEnded(pollID)
    if operation == "revealPeriodActive":
        if len(args) != 1:
            return False
        pollID = args[0]
        return revealPeriodActive(pollID)
    if operation == "commitPeriodActive":
        if len(args) != 1:
            return False
        pollID = args[0]
        return commitPeriodActive(pollID)
    if operation == "didCommit":
        if len(args) != 2:
            return False
        account = args[0]
        pollID = args[1]
        return didCommit(account, pollID)
    if operation == "didReveal":
        if len(args) != 2:
            return False
        account = args[0]
        pollID = args[1]
        return didReveal(account, pollID)
    if operation == "pollExists":
        if len(args) != 1:
            return False
        pollID = args[0]
        return pollExists(pollID)
    if operation == "getCommitHash":
        if len(args) != 2:
            return False
        voter = args[0]
        pollID = args[1]
        return getCommitHash(voter, pollID)
    if operation == "getNumTokens":
        if len(args) != 2:
            return False
        voter = args[0]
        pollID = args[1]
        return getNumTokens(voter, pollID)
    if operation == "getLastNode":
        if len(args) != 1:
            return False
        voter = args[0]
        return getLastNode(voter)
    if operation == "getLockedTokens":
        if len(args) != 1:
            return False
        voter = args[0]
        return getLockedTokens(voter)
    if operation == "getPollNounce":
        return getPollNounce()
    if operation == "isExpired":
        if len(args) != 1:
            return False
        terminationDate = args[0]
        return isExpired(terminationDate)
    if operation == "attrUUID":
        if len(args) != 2:
            return False
        user = args[0]
        pollID = args[1]
        return attrUUID(user, pollID)
    if operation == "getEndTimeList":
        if len(args) != 1:
            return False
        pollID = args[0]
        return getEndTimeList(pollID)

    return False

def init(reversedTokenHash):
    assert(CheckWitness(Admin))
    if not Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH):
        Put(GetContext(), TOKEN_CONTRACT_REVERSED_HASH, reversedTokenHash)
        Notify(["Contract Initialized Successfully!"])
        return True
    else:
        Notify(["Contract already Initialized!"])
        return False

def reSetTokenHash(reversedTokenHash):
    assert(CheckWitness(Admin))
    assert(len(reversedTokenHash) == 20)
    Put(GetContext(), TOKEN_CONTRACT_REVERSED_HASH, reversedTokenHash)
    Notify(["reSetTokenHash", reversedTokenHash])
    return True


def requestVotingRights(account, numTokens):
    assert(CheckWitness(account))
    tokenHash = getTokenHash()
    # check that the actual token balance of the message sender is sufficient relative to the numTokens argument provided
    params = [account]
    res = DynamicAppCall(tokenHash, "balanceOf", params)
    assert(res >= numTokens)
    # transfer numTokens of tokens from account to the contract
    params = [account, SelfContractHash, numTokens]
    res = DynamicAppCall(tokenHash, "transfer", params)
    assert(res)
    # update the account's vote token balance
    Put(GetContext(), _concatKey(VOTE_TOKEN_BALANCE, account), Add(getVoteTokenBalance(account), numTokens))
    Notify(["votingRightsGranted", account, numTokens])
    return True


def withdrawVotingRights(account, numTokens):
    assert(CheckWitness(account))
    availableTokens = Sub(getVoteTokenBalance(account), getLockedTokens(account))
    # numTokens should not be greater than the account's vote token balance
    assert(numTokens <= availableTokens)

    # update the account's vote token balance
    Put(GetContext(), _concatKey(VOTE_TOKEN_BALANCE, account), Sub(getVoteTokenBalance(account), numTokens))

    # transfer numTokens of tokens from the contract to account
    params = [SelfContractHash, account, numTokens]
    res = DynamicAppCall(getTokenHash(), "transfer", params)
    assert(res)

    Notify(["votingRightsWithdrawn", account, numTokens])
    return True

def rescueTokens(voter, pollID):
    assert(CheckWitness(voter))
    pollRevealEndTime = Get(GetContext(), _concatKey(POLL_REVEAL_END_KEY, pollID))
    assert(isExpired(pollRevealEndTime))
    # check if prevPollID exists in the voter's DLL
    dllData = getVoterDllData(voter)
    assert(dllData.has_key(str(pollID)))

    key = _concatKey(DLL_MAP_KEY, voter)
    dllData = _remove(dllData, pollID)
    Put(GetContext(), key, Serialize(dllData))

    Notify(["tokenRescued", pollID, voter])
    return True

def rescueTokensInMultiplePolls(voterList, pollIDList):
    lenList = len(voterList)
    assert(lenList == len(pollIDList))
    i = 0
    while i < lenList:
        voter = voterList[i]
        pollID = pollIDList[i]
        assert(rescueTokens(voter, pollID))
    return True


def getTokenHash():
    return Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)

def getVoteTokenBalance(account):
    return Get(GetContext(), _concatKey(VOTE_TOKEN_BALANCE, account))


def commitVote(voter, pollID, secretHash, numTokens, prevPollID):
    assert(CheckWitness(voter))
    assert(commitPeriodActive(pollID))
    # if voter doesn't have enough voting rights, request for enough voting rights
    voterTokenBalance = getVoteTokenBalance(voter)
    if  voterTokenBalance< numTokens:
        remainder = Sub(numTokens, voterTokenBalance)
        assert(requestVotingRights(voter, remainder) == True)
    # make sure voter has enough voting rights
    assert(getVoteTokenBalance(voter) >= numTokens)
    # prevent voter from committing to zero node placeholder
    assert(pollID != 0)
    # prevent voter from committing a secretHash of 0
    assert(secretHash != 0)
    # check if prevPollID exists in the voter's DLL or if prevPollID is 0
    dllData = getVoterDllData(voter)
    assert(prevPollID == 0 or dllData.has_key(str(prevPollID)))
    nextPollID = getNext(dllData, prevPollID)
    # edge case: in-place update
    if nextPollID == pollID:
        nextPollID = getNext(dllData, pollID)
    assert(validPosition(prevPollID, nextPollID, voter, numTokens))
    key = _concatKey(DLL_MAP_KEY, voter)
    dllData = _insert(dllData, prevPollID, pollID, nextPollID)
    Put(GetContext(), key, Serialize(dllData))
    UUID = attrUUID(voter, pollID)
    setAttribute(UUID, "numTokens", numTokens)
    # setAttribute(UUID, "commitHash", int(secretHash))
    setAttribute(UUID, "commitHash", secretHash)
    # update commit status
    Put(GetContext(), _concatKey(_concatKey(POLL_DID_COMMIT_KEY, pollID), voter), 1)
    Notify(["voteCommitted", pollID, numTokens, voter])
    return True


def commitVotes(voterList, pollIDList, secretHashList, numTokensList, prevPollIDList):
    # make sure the array or list length are all the same
    listLen = len(voterList)
    assert(listLen == len(pollIDList))
    assert(listLen == len(secretHashList))
    assert(listLen == len(numTokensList))
    assert(listLen == len(prevPollIDList))
    i = 0
    while i < listLen:
        voter = voterList[i]
        pollID = pollIDList[i]
        secretHash = secretHashList[i]
        numToken = numTokensList[i]
        prevPollID = prevPollIDList[i]
        assert(commitVote(voter, pollID, secretHash, numToken, prevPollID) == True)
        i = i + 1
    return True


def validPosition(prevID, nextID, voter, numTokens):
    prevValid = numTokens >= getNumTokens(voter, prevID)
    # if next is zero node, numTokens does not need to be greater
    nextValid = numTokens <= getNumTokens(voter, nextID) or nextID == 0
    return prevValid and nextValid


def revealVote(voter, pollID, voteOption, salt):
    assert(CheckWitness(voter))
    # make sure the reveal period is active
    assert(revealPeriodActive(pollID))
    assert(didCommit(voter, pollID))
    assert(not didReveal(voter, pollID))
    # compare resultant hash from inputs to original commitHash
    assert(sha256(_concatKey(voteOption, salt)) == getCommitHash(voter, pollID))

    numTokens = getNumTokens(voter, pollID)

    forKey = _concatKey(POLL_VOTES_FOR_KEY, pollID)
    forNumTokens = Get(GetContext(), forKey)

    againstKey = _concatKey(POLL_VOTES_AGAINSt_KEY, pollID)
    againstNumTokens = Get(GetContext(), againstKey)
    if voteOption == 1:
        forNumTokens = Add(forNumTokens, numTokens)
        Put(GetContext(), forKey, forNumTokens)
    else:
        againstNumTokens = Add(againstNumTokens, numTokens)
        Put(GetContext(), againstKey, againstNumTokens)
    dllData = getVoterDllData(voter)
    key = _concatKey(DLL_MAP_KEY, voter)
    dllData = _remove(dllData,pollID)
    Put(GetContext(), key, Serialize(dllData))

    Put(GetContext(), _concatKey(_concatKey(POLL_DID_REVEAL_KEY, pollID), voter), 1)
    Put(GetContext(), _concatKey(_concatKey(POLL_VOTE_OPTIONS_KEY, pollID), voter), voteOption)
    Notify(["voteRevealed", pollID, numTokens, forNumTokens, againstNumTokens, voteOption, voter, salt])

    return True

def revealVotes(voterList, pollIDList, voteOptionList, saltList):
    listLen = len(voterList)
    assert(listLen == len(pollIDList))
    assert(listLen == len(voteOptionList))
    assert(listLen == len(saltList))
    i = 0
    while i < listLen:
        voter = voterList[i]
        pollID = pollIDList[i]
        voteOption = voteOptionList[i]
        salt = saltList[i]
        assert(revealVote(voter, pollID, voteOption, salt) == True)
        i = i + 1
    return True


def getNumPassingTokens(voter, pollID):
    assert(pollEnded(pollID))

    assert(didReveal(voter, pollID))

    winnningChoice = 0
    if isPassed(pollID):
        winnningChoice = 1
    voterVoteOption = Get(GetContext(), _concatKey(_concatKey(POLL_VOTE_OPTIONS_KEY, pollID), voter))
    if voterVoteOption == winnningChoice:
        return getNumTokens(voter, pollID)
    else:
        return 0


def startPoll(voteQuorum, commitDuration, revealDuration):
    # update poll nounce
    Put(GetContext(), POLL_NOUNCE_KEY, Add(getPollNounce(), 1))

    commitEndTime = Add(GetTime(), commitDuration)
    revealEndTime = Add(commitEndTime, revealDuration)

    pollNounce = getPollNounce()
    Put(GetContext(), _concatKey(POLL_VOTE_QUORUM_KEY, pollNounce), voteQuorum)
    Put(GetContext(), _concatKey(POLL_COMMIT_END_KEY, pollNounce), commitEndTime)
    Put(GetContext(), _concatKey(POLL_REVEAL_END_KEY, pollNounce), revealEndTime)
    Notify(["pollCreated", voteQuorum, commitEndTime, revealEndTime, pollNounce])
    return pollNounce


def isPassed(pollID):
    assert(pollEnded(pollID))
    votesFor = Get(GetContext(), _concatKey(POLL_VOTES_FOR_KEY, pollID))
    votesAgainst = Get(GetContext(), _concatKey(POLL_VOTES_AGAINSt_KEY, pollID))
    voteQuorum = Get(GetContext(), _concatKey(POLL_VOTE_QUORUM_KEY, pollID))
    return 100 * votesFor > voteQuorum * (votesFor + votesAgainst)


def getTotalNumberOfTokensForWinningOption(pollID):
    assert(pollEnded(pollID))
    if isPassed(pollID):
        votesFor = Get(GetContext(), _concatKey(POLL_VOTES_FOR_KEY, pollID))
        return votesFor
    else:
        votesAgainst = Get(GetContext(), _concatKey(POLL_VOTES_AGAINSt_KEY, pollID))
        return votesAgainst


def pollEnded(pollID):
    assert(pollExists(pollID))
    revealEndTime = Get(GetContext(), _concatKey(POLL_REVEAL_END_KEY, pollID))
    return isExpired(revealEndTime)


def revealPeriodActive(pollID):
    assert(pollExists(pollID))
    pollRevealEndTime = Get(GetContext(), _concatKey(POLL_REVEAL_END_KEY, pollID))
    pollRevealExpired =  isExpired(pollRevealEndTime)
    pollCommitExpired = not commitPeriodActive(pollID)
    return (not pollRevealExpired) and pollCommitExpired


def commitPeriodActive(pollID):
    assert(pollExists(pollID))
    pollCommitEndTime = Get(GetContext(), _concatKey(POLL_COMMIT_END_KEY, pollID))
    pollCommitPeriodExpired = isExpired(pollCommitEndTime)
    return not pollCommitPeriodExpired


def didCommit(account, pollID):
    """
    :param account:  voter
    :param pollID:
    :return: 1 means did reveal, 0 or NULL means NOT
    """
    assert(pollExists(pollID))
    return Get(GetContext(), _concatKey(_concatKey(POLL_DID_COMMIT_KEY, pollID), account))

def didReveal(account, pollID):
    """
    :param account: voter
    :param pollID:
    :return: 1 means did reveal, 0 or NULL means NOT
    """
    assert(pollExists(pollID))
    return Get(GetContext(), _concatKey(_concatKey(POLL_DID_REVEAL_KEY, pollID), account))

def pollExists(pollID):
    if not pollID:
        return False
    if pollID <= getPollNounce():
        return True
    else:
        return False

def getCommitHash(voter, pollID):
    return getAttribute(attrUUID(voter, pollID), "commitHash")

def getNumTokens(voter, pollID):
    return getAttribute(attrUUID(voter, pollID), "numTokens")

def getLastNode(voter):
    dllData = getVoterDllData(voter)
    return getPrev(dllData, 0)

def getLockedTokens(voter):
    return getNumTokens(voter, getLastNode(voter))

def getPollNounce():
    return Get(GetContext(), POLL_NOUNCE_KEY)


def isExpired(terminationDate):
    return GetTime() > terminationDate

def attrUUID(user, pollID):
    return sha256(_concatKey(user, pollID))


def getVoterDllData(voter):
    """
    :param voter:
    :return: Deserialized MAP
    """
    dllDataInfo = Get(GetContext(), _concatKey(DLL_MAP_KEY, voter))
    dllData = {}
    if dllDataInfo:
        dllData = Deserialize(dllDataInfo)
    return dllData


def getEndTimeList(pollID):
    pollCommitEndTime = Get(GetContext(), _concatKey(POLL_COMMIT_END_KEY, pollID))
    pollRevealEndTime = Get(GetContext(), _concatKey(POLL_REVEAL_END_KEY, pollID))
    return [pollCommitEndTime, pollRevealEndTime]


def _concatKey(str1, str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)


def setAttribute(UUID, attrName, attrVal):
    key = _concatKey(UUID, attrName)
    Put(GetContext(), key, attrVal)

def getAttribute(UUID, attrName):
    key = _concatKey(UUID, attrName)
    return Get(GetContext(), key)

# def attachAttribute(UUID, attrName, attrVal):
#     key = _concatKey(UUID, attrName)
#     Put(GetContext(), key, attrVal)
#     return True


def getNext(data, curr):
    """
    :param data: Deserialized MAP, key is str(int), value is Serialize([int1, int2])
    :param curr: int
    :return: int
    """
    currStr = str(curr)
    if data.has_key(currStr):
        nodeListInfo = data[currStr]
        nodeList = [0, 0]
        if nodeListInfo:
            nodeList = Deserialize(nodeListInfo)
        # nodeList is a node, which is a list, the first element corresponds with prev, the second co-with next
        return nodeList[1]
    return 0

def getPrev(data, curr):
    """

    :param data: Deserialized MAP, key is str(int), value is Serialize([int1, int2])
    :param curr: int
    :return: int
    """
    currStr = str(curr)
    if data.has_key(currStr):
        nodeListInfo = data[currStr]
        nodeList = [0, 0]
        if nodeListInfo:
            nodeList = Deserialize(nodeListInfo)
        return nodeList[0]
    return 0

def _insert(data, prev, curr, next):
    """
    :param data: Deserialized MAP, key is str(int), value is Serialize([int1, int2])
    :param prev: int
    :param curr: int
    :param next: int
    :return: Deserialized MAP
    """
    currStr = str(curr)
    nextStr = str(next)
    prevStr = str(prev)

    # nodeList = [0, 0]
    # if cNodeInfo:
    #     nodeList = Deserialize(cNodeInfo)
    cNode = [0, 0]
    if data.has_key(currStr):
        cNodeInfo = data[currStr]
        if cNodeInfo:
            cNode = Deserialize(cNodeInfo)

    cNode[0] = prev
    cNode[1] = next
    data[currStr] = Serialize(cNode)

    # nNodeInfo = data[nextStr]
    # nNode = [0, 0]
    # if nNodeInfo:
    #     nNode = Deserialize(nNodeInfo)
    nNode = [0, 0]
    if data.has_key(nextStr):
        nNodeInfo = data[nextStr]
        if nNodeInfo:
            nNode = Deserialize(nNodeInfo)

    nNode[0] = curr
    data[nextStr] = Serialize(nNode)


    # pNodeInfo = data[prevStr]
    # pNode = [0, 0]
    # if pNodeInfo:
    #     pNode = Deserialize(pNodeInfo)
    pNode = [0, 0]
    if data.has_key(prevStr):
        pNodeInfo = data[prevStr]
        if pNodeInfo:
            pNode = Deserialize(pNodeInfo)

    pNode[1] = curr
    data[prevStr] = Serialize(pNode)
    return data

def _remove(data, curr):
    """
    :param data: Deserialized MAP, key is str(int), value is Serialize([int1, int2])
    :param curr: int
    :return: Deserialized MAP,
    """
    currStr = str(curr)
    next = getNext(data, curr)
    nextStr = str(next)
    prev = getPrev(data, curr)
    prevStr = str(prev)

    # nNodeInfo = data[nextStr]
    # nNode = [0, 0]
    # if nNodeInfo:
    #     nNode = Deserialize(nNodeInfo)
    nNode = [0, 0]
    if data.has_key(nextStr):
        nNodeInfo = data[nextStr]
        if nNodeInfo:
            nNode = Deserialize(nNodeInfo)
    nNode[0] = prev
    data[nextStr] = Serialize(nNode)


    # pNodeInfo = data[prevStr]
    # pNode = [0, 0]
    # if pNodeInfo:
    #     pNode = Deserialize(pNodeInfo)
    pNode = [0, 0]
    if data.has_key(prevStr):
        pNodeInfo = data[prevStr]
        if pNodeInfo:
            pNode = Deserialize(pNodeInfo)
    pNode[1] = next
    data[prevStr] = Serialize(pNode)

    # data[currStr] = Serialize([curr, curr])
    if data.has_key(currStr):
        data.remove(currStr)

    return data

def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    assert(c >= a)
    return c

def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    assert(a>=b)
    return a-b
