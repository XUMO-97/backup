# State Registry

The state registry is a smart contract that stores the state of the state machine and handles state applications.

The state registry has a large API, but here we will only focus on the functions and events that are particularly relevant to the operator (i.e. the game developer).

## Functions

### apply

Submit a state application.

```solidity
function apply(bytes32 _key, uint _amount, string _data)
```

- `key`: a unique identifier that identifies the application.
- `amount`: the amount of tokens to stake for the application. It must be at least as large as `minDeposit` as specified in [the config](./docs/registry-factory-config-example.json). Before calling apply, you need to ensure that you've [approved](https://theethereum.wiki/w/index.php/ERC20_Token_Standard#Approve_And_TransferFrom_Token_Balance) the registry contract to transfer at least `amount` tokens.
- `data`: the value of the application. If the value is large enough that you don't want to store it on the blockchain, you could also store it in IPFS and use an IPFS hash.

It's recommended that the `key` is a `keccak256` hash. For instance, if `data` is a JSON object that looks like:

```json
{
  "matchID": 281975,
  "winnerDragon": 98325720
}
```

Then you could use the hash of `matchID` as the key.

Note that it's recommended that the application is "immutable," meaning that the application refers to a fact at a particular moment in time. For instance, instead of applying "the level of dragon A", it's better to apply "the level of dragon A as of nonce 568927". This is because if you use the former, once the dragon levels up again, the application will cease to be valid and may be successfully challenged, which means you may lose your stake.

### updateStatus

Once `applyStageLength` seconds (see `registry-factory-config-example.json`) have passed, anyone may call `updateStatus` to confirm the application, i.e. writing it into the registry if it has not been successfully challenged.

Note that without calling this function, the application won't actually be written into the registry. Therefore it's important that someone calls this function.

```solidity
function updateStatus(bytes32 _key)
```

### getData

Get the data for a application.

```solidity
function getData(bytes32 _key) returns (bool exists, string data)
```

- `key`: the unique identifier for the application.
- `exists`: indicates whether the state application exists. If `exists` is `false`, `data` is an empty string.
- `data`: the value of the application.

### exit

Remove an entry from the state registry. The staked tokens will be returned to the owner of the entry. Only the owner of the entry can call this function.

```solidity
function exit(bytes32 _key)
```

## Events

### Application

```solidity
event _Application(bytes32 indexed key, uint deposit, uint applyStageLen, uint appEndDate, string value, address indexed applicant);
```

This event is emitted when an application has been made.

### ApplicationWhitelisted

```solidity
event _ApplicationWhitelisted(bytes32 indexed key)
```

This event is emitted when an application (i.e. a application) has been accepted.

## Config

Here we explain the fields in the config. [Here's a full example](./docs/registry-factory-config-example.json).

See [PLCR voting](https://github.com/ConsenSys/PLCRVoting) for what `commit` and `reveal` means.

- `minDeposit`: the minimum amount of tokens that needs to be staked when creating an application.
- `applyStageLength`: the number of seconds that the apply stage lasts. The apply stage starts when `apply` is called. Only during the apply stage can the application be challenged.
- `commitStageLength`: the number of seconds that the reveal stage lasts. The commit stage starts when an application has been challenged. Only during the commit stage can people vote on the application.
- `revealStageLength`: the number of seconds that the reveal stage lasts. The reveal stage starts when the commit stage ends. Only during the reveal stage can people reveal their votes.
- `dispensationPct`: when someone wins a challenge, they will get back their own deposit, plus a sum of tokens equal to the `dispensationPct` of their opponent’s stake.
- `voteQuorum`: the percentage of votes it takes for an application to be considered accepted.

Each of these parameters has a variant starting with `p`, like `minDeposit` and `pMinDeposit`. The `p` variants are for adjusting the parameters themselves. For instance, if `pMinDeposit` is 100, it means that the minimum deposit for submitting an application that changes a parameter is 100.
