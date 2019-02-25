OntCversion = '2.0.0'
"""
Parameterizer Smart Contract
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
from contracts.libs.SafeMath import Add, Sub, Mul, Div

TOKEN_CONTRACT_REVERSED_HASH = "ContractHash"
PLCR_CONTRACT_REVERSED_HASH = "PLCRContractHash"

Owner = Base58ToAddress("ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS")

SelfContractHash = GetExecutingScriptHash()

MIN_DEPOSIT_KEY = "minDeposit"
P_MIN_DEPOSIT_KEY = "pMinDeposit"
APPLY_STAGE_LEN_KEY = "applyStageLen"
P_APPLY_STAGE_LEN_KEY = "pApplyStageLen"
COMMIT_STAGE_LEN_KEY = "commitStageLen"
P_COMMIT_STAGE_LEN_KEY = "pCommitStageLen"
REVEAL_STAGE_LEN_KEY = "revealStageeLen"
P_REVEAL_STAGE_LEN_KEY = "pRevealStageLen"
DISPENSATION_PCT_KEY = "dispensationPct"
P_DISPENSATION_PCT_KEY = "pDispensationPct"
VOTE_QUORUM_KEY = "voteQuorum"
P_VOTE_QUORUM_KEY = "pVoteQuorum"
OPERATOR_KEY = "operator"


# # PARAM_APP_EXPIREY + propID  ----- store intended data change if poll passes
# PARAM_APP_EXPIREY = "P1"
# PARAM_CHALLENGE_ID = "P2"
# PARAM_DEPOSIT = "P3"
# PARAM_NAME = "P4"
# PARAM_OWNER = "P5"
# PARAM_PROCESS_BY = "P6"
# PARAM_VALUE = "P7"


# PROPOSAL_KEY + propID  ----- store intended data change if poll passes
PROPOSAL_MAP_KEY = "ParamProposal"

# CHALLENGE_MAP_KEY + pollID ---  store associated challenge data except tokenClaims
CHALLENGE_MAP_KEY = "Challenge"
# CHALLENGE_TOKEN_CLAIMS_KEY + pollID + address --- store
CHALLENGE_TOKEN_CLAIMS_KEY = "C1"

# 7 days
ProcessBy = 604800

def Main(operation, args):
    if operation == "init":
        if len(args) != 4:
            return False
        tokenRCH = args[0]
        plcrRCH = args[1]
        parametersList = args[2]
        operator = args[3]
        return init(tokenRCH, plcrRCH, parametersList, operator)
    if operation == "proposeReparameterization":
        if len(args) != 2:
            return False
        name = args[0]
        value = args[1]
        return proposeReparameterization(name, value)
    if operation == "challengeReparameterization":
        if len(args) != 2:
            return False
        challenger = args[0]
        propID = args[1]
        return challengeReparameterization(challenger, propID)
    if operation == "processProposal":
        if len(args) != 1:
            return False
        propID = args[0]
        return processProposal(propID)
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
    if operation == "canBeSet":
        if len(args) != 1:
            return False
        propID = args[0]
        return canBeSet(propID)
    if operation == "propExists":
        if len(args) != 1:
            return False
        propID = args[0]
        return propExists(propID)
    if operation == "challengeCanBeResolved":
        if len(args) != 1:
            return False
        propID = args[0]
        return challengeCanBeResolved(propID)
    if operation == "challengeWinnerReward":
        if len(args) != 1:
            return False
        challengeID = args[0]
        return challengeWinnerReward(challengeID)
    if operation == "get":
        if len(args) != 1:
            return False
        name = args[0]
        return get(name)
    if operation == "getOperator":
        return getOperator()
    if operation == "tokenClaims":
        if len(args) != 2:
            return False
        challengeID = args[0]
        voter = args[1]
        return tokenClaims(challengeID, voter)

    return False


# RCH means reversed contract hash
def init(tokenRCH, plcrRCH, parametersList, operator):
    assert(CheckWitness(Owner))
    assert(len(plcrRCH) == 20)
    assert(len(tokenRCH) == 20)

    Put(GetContext(), TOKEN_CONTRACT_REVERSED_HASH, tokenRCH)
    Put(GetContext(), PLCR_CONTRACT_REVERSED_HASH, plcrRCH)

    Put(GetContext(), MIN_DEPOSIT_KEY, parametersList[0])
    Put(GetContext(), P_MIN_DEPOSIT_KEY, parametersList[1])

    Put(GetContext(), APPLY_STAGE_LEN_KEY, parametersList[2])
    Put(GetContext(), P_APPLY_STAGE_LEN_KEY, parametersList[3])

    Put(GetContext(), COMMIT_STAGE_LEN_KEY, parametersList[4])
    Put(GetContext(), P_COMMIT_STAGE_LEN_KEY, parametersList[5])

    Put(GetContext(), REVEAL_STAGE_LEN_KEY, parametersList[6])
    Put(GetContext(), P_REVEAL_STAGE_LEN_KEY, parametersList[7])

    Put(GetContext(), DISPENSATION_PCT_KEY, parametersList[8])
    Put(GetContext(), P_DISPENSATION_PCT_KEY, parametersList[9])

    Put(GetContext(), VOTE_QUORUM_KEY, parametersList[10])
    Put(GetContext(), P_VOTE_QUORUM_KEY, parametersList[11])

    Put(GetContext(), OPERATOR_KEY, operator)

    return True

def proposeReparameterization(name, value):
    assert(CheckWitness(Owner))
    deposit = Get(GetContext(), P_MIN_DEPOSIT_KEY)
    propID = sha256(_concatKey(name, value))
    if name == DISPENSATION_PCT_KEY or name == P_DISPENSATION_PCT_KEY:
        assert(value <= 100)
    # Forbid duplicate proposals
    assert(not propExists(propID))
    # Forbid NOOP reparameterizations
    assert(Get(GetContext(), name) != value)
    # attach name and value to pollID
    pApplyStageLen = Get(GetContext(), P_APPLY_STAGE_LEN_KEY)
    pCommitStageLen = Get(GetContext(), P_COMMIT_STAGE_LEN_KEY)
    pRevealStageLen = Get(GetContext(), P_REVEAL_STAGE_LEN_KEY)
    appExpiry = Add(GetTime(), pApplyStageLen)
    proposal = {
        "appExpiry": appExpiry,
        "challengeID": 0,
        "deposit": deposit,
        "name": name,
        "owner": Owner,
        "processBy": Add(GetTime(), Add(pApplyStageLen, Add(pCommitStageLen, Add(pRevealStageLen, ProcessBy)))),
        "value": value
    }
    Put(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID), Serialize(proposal))

    tokenHash = Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)
    res = DynamicAppCall(tokenHash, "transfer", [Owner, SelfContractHash, deposit])
    assert(res)
    Notify(["reparameterizationProposal", name, value, propID, deposit, appExpiry, Owner])
    return propID


def challengeReparameterization(challenger, propID):
    assert(CheckWitness(challenger))
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        # Error: 101 means propID does not exist
        Notify(["Error", 101])
        return False
    proposal = Deserialize(proposalInfo)
    assert(propExists(propID) and proposal["challengeID"] == 0)
    deposit = proposal["deposit"]
    # start poll
    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    pVoteQuorum = Get(GetContext(), P_VOTE_QUORUM_KEY)
    pCommitStageLen = Get(GetContext(), P_COMMIT_STAGE_LEN_KEY)
    pRevealStageLen = Get(GetContext(), P_REVEAL_STAGE_LEN_KEY)
    params = [pVoteQuorum, pCommitStageLen, pRevealStageLen]
    pollID = DynamicAppCall(plcrHash, "startPoll", params)
    pDispensationPct = Get(GetContext(), P_DISPENSATION_PCT_KEY)
    challenge = {
        "challenger": challenger,
        "rewardPoll": Div(Mul(Sub(100, pDispensationPct), deposit), 100),
        "stake": deposit,
        "resolved": False,
        "winningTokens": 0
    }
    Put(GetContext(), _concatKey(CHALLENGE_MAP_KEY, pollID), Serialize(challenge))
    # update listing to store most recent challenge
    proposal["challengeID"] = pollID
    Put(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID), Serialize(proposal))

    # take tokens from challenger
    tokenHash = Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)
    params = [challenger, SelfContractHash, deposit]
    res = DynamicAppCall(tokenHash, "transfer", params)
    assert(res)

    endTimeList = DynamicAppCall(plcrHash, "getEndTimeList", [pollID])
    commitEndTime = endTimeList[0]
    revealEndTime = endTimeList[1]
    Notify(["newChallenge", propID, pollID, commitEndTime, revealEndTime, challenger])
    return pollID


def processProposal(propID):
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        # Error: 201, proposal corresponding with propID does not exist.
        Notify(["Error", 201])
        return False
    proposal = Deserialize(proposalInfo)
    propOwner = proposal["owner"]
    propDeposit = proposal["deposit"]

    tokenHash = Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)

    # Before any token transfers, deleting the proposal will ensure that if reentrancy occurs the
    # prop.owner and prop.deposit will be 0, thereby preventing theft
    if canBeSet(propID):
        # There is no challenge against the proposal. The processBy date for the proposal has not
        # passed, but the proposal's appExpirty date has passed.
        name = proposal["name"]
        value = proposal["value"]
        Put(GetContext(), name, value)
        Notify(["proposalAccepted", name, value])
        Delete(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
        params = [SelfContractHash, propOwner, propDeposit]
        res = DynamicAppCall(tokenHash, "transfer", params)
        assert(res)
    elif challengeCanBeResolved(propID):
        # There is a challenge against the proposal
        _resolveChallenge(propID)
    elif GetTime() > proposal["processBy"]:
        # there is no challenge against the proposal, but the processBy date has passed
        Notify(["proposalExpired", propID])
        Delete(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
        params = [SelfContractHash, propOwner, propDeposit]
        res = DynamicAppCall(tokenHash, "transfer", params)
        assert (res)
    else:
        # there is no challenge against the proposal, and neither the appExpiry date
        # or the processBy data has passed
        raise Exception("rollBack!")

    dispensationPct = Get(GetContext(), DISPENSATION_PCT_KEY)
    pDispensationPct = Get(GetContext(), P_DISPENSATION_PCT_KEY)
    assert(dispensationPct <= 100)
    assert(pDispensationPct <= 100)

    # verify that future proposal appExpiry and processBy times will not overflow
    pApplyStageLen = Get(GetContext(), P_APPLY_STAGE_LEN_KEY)
    pCommitStageLen = Get(GetContext(), P_COMMIT_STAGE_LEN_KEY)
    pRevealStageLen = Get(GetContext(), P_REVEAL_STAGE_LEN_KEY)
    useLess = Add(GetTime(), Add(pApplyStageLen, Add(pCommitStageLen, Add(pRevealStageLen, ProcessBy))))
    Delete(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    return True


def claimReward(account, challengeID):
    # ensure voter has not already claimed tokens and challenge results have been processed
    assert(CheckWitness(account))

    # tokenClaim = Get(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), account))
    tokenClaim = tokenClaims(challengeID, account)

    assert(tokenClaim == False)
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        return False
    challenge = Deserialize(challengeInfo)
    assert(challenge["resolved"] == True)

    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    voterTokens = DynamicAppCall(plcrHash, "getNumPassingTokens", [account, challengeID])
    reward = voterReward(account, challengeID)

    # subtract voter's information to preserve the participation ratios of other voters
    # compared to the remaining pool of rewards
    challenge["winningTokens"] = Sub(challenge["winningTokens"], voterTokens)
    challenge["rewardPool"] = Sub(challenge["rewardPool"], reward)

    # ensure a voter cannot claim token again
    Put(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), account), True)

    Notify(["rewardClaimed", challengeID, reward, account])

    tokenHash = Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)
    params = [SelfContractHash, account, reward]
    res = DynamicAppCall(tokenHash, "transfer", params)
    assert(res)

    return True

def claimRewards(accountList, challengeIDList):
    # make sure the array lengths are the same
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
        return False
    challenge = Deserialize(challengeInfo)
    winningTokens = challenge["winningTokens"]
    rewardPoll = challenge["rewardPool"]
    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    voterTokens = DynamicAppCall(plcrHash, "getNumPassingTokens", [voter, challengeID])
    return Div(Mul(voterTokens, rewardPoll), winningTokens)


def canBeSet(propID):
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        return False
    proposal = Deserialize(proposalInfo)
    if not proposal.has_key("appExpiry"):
        return False
    now = GetTime()
    afterAppExpiry = now > proposal["appExpiry"]
    beforeProcessBy = now < proposal["processBy"]
    noChallengeID = proposal["challengeID"] == 0
    return afterAppExpiry and beforeProcessBy and noChallengeID

def propExists(propID):
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        return False
    proposal = Deserialize(proposalInfo)
    if not proposal.has_key("processBy"):
        return False
    return proposal["processBy"] > 0

def challengeCanBeResolved(propID):
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        return False
    proposal = Deserialize(proposalInfo)
    if not proposal.has_key("challengeID"):
        return False
    challengeID = proposal["challengeID"]
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        return False
    challenge = Deserialize(challengeInfo)
    challengeIDGTZ = challengeID > 0
    challengeNotResolved = challenge["resolved"] == False
    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    votePollEndedRes = DynamicAppCall(plcrHash, "pollEnded", [challengeID])
    return challengeIDGTZ and challengeNotResolved and votePollEndedRes



def challengeWinnerReward(challengeID):
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        return False
    challenge = Deserialize(challengeInfo)
    stake = challenge["stake"]

    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    totalNumberOfTokensForWinningOption = DynamicAppCall(plcrHash, "getTotalNumberOfTokensForWinningOption", [challengeID])
    if totalNumberOfTokensForWinningOption == 0:
        # edge case, nobody voted, give all tokens to the challenger
        return Mul(2, stake)

    rewardPool = challenge["rewardPoll"]
    return Sub(Mul(2, stake), rewardPool)

def get(name):
    return Get(GetContext(), name)

def getOperator():
   return Get(GetContext(), OPERATOR_KEY)

def tokenClaims(challengeID, voter):
    return Get(GetContext(), _concatKey(_concatKey(CHALLENGE_TOKEN_CLAIMS_KEY, challengeID), voter))


def _resolveChallenge(propID):
    proposalInfo = Get(GetContext(), _concatKey(PROPOSAL_MAP_KEY, propID))
    if not proposalInfo:
        # Error: 201, proposal corresponding with propID does not exist.
        Notify(["Error", 301])
        return False
    proposal = Deserialize(proposalInfo)
    if not proposal.has_key("challengeID"):
        return False

    challengeID = proposal["challengeID"]
    challengeInfo = Get(GetContext(), _concatKey(CHALLENGE_MAP_KEY, challengeID))
    if not challengeInfo:
        return False
    challenge = Deserialize(challengeInfo)

    # winner gets back their full staked deposit, and dispensationPct*loser's stake
    reward = challengeWinnerReward(challengeID)

    plcrHash = Get(GetContext(), PLCR_CONTRACT_REVERSED_HASH)
    totalNumberOfTokensForWinningOption = DynamicAppCall(plcrHash, "getTotalNumberOfTokensForWinningOption", [challengeID])
    challenge["winningTokens"] = totalNumberOfTokensForWinningOption
    challenge["resolved"] = True

    params = [challengeID]
    isPassedRes = DynamicAppCall(plcrHash, "isPassed", params)
    tokenHash = Get(GetContext(), TOKEN_CONTRACT_REVERSED_HASH)
    if isPassedRes:
        # The challenge failed
        if proposal["processBy"] > GetTime():
            Put(GetContext(), proposal["name"], proposal["value"])
        Notify(["challengeFailed", propID, challengeID, challenge["rewardPoll"], challenge["winningTokens"]])
        params = [SelfContractHash, proposal["owner"], reward]
        res = DynamicAppCall(tokenHash, "transfer", params)
        assert(res)
    else:
        # The challenge succeeded or nobody voted
        Notify(["challengeSucceeded", propID, challengeID, challenge["rewardPoll"], challenge["winningTokens"]])
        params = [SelfContractHash, challenge["challenger"], reward]
        res = DynamicAppCall(tokenHash, "transfer", params)
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