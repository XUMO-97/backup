const fs = require('fs');
const ssbUtils = require('ssb-keys/util');
const web3Utils = require('web3-utils')

const RegistryFactory = artifacts.require('RegistryFactory.sol');

const config = JSON.parse(fs.readFileSync('../conf/config.json'));
const paramConfig = config.paramDefaults;

// Convert a number to BN, with decimals multiplied
function toBN(x, decimals) {
    return web3Utils.toBN(x).mul(web3Utils.toBN(10).pow(web3Utils.toBN(decimals)))
}

module.exports = (callback) => {
    async function deployRegistry() {
        const registryFactory = await RegistryFactory.deployed();
        let registryReceipt;
        // Truffle's contract (or web3's) require that a bytes32 argument
        // be passed as hex-encoded strings.
        const operator = web3Utils.bytesToHex(ssbUtils.toBuffer(config.operator));
        const decimals = config.token.decimals;
        if (config.token.deployToken) {
            registryReceipt = await registryFactory.newRegistryWithToken(
                config.token.supply,
                config.token.name,
                config.token.decimals,
                config.token.symbol,
                [
                    toBN(paramConfig.minDeposit, decimals),
                    toBN(paramConfig.pMinDeposit, decimals),
                    paramConfig.applyStageLength,
                    paramConfig.pApplyStageLength,
                    paramConfig.commitStageLength,
                    paramConfig.pCommitStageLength,
                    paramConfig.revealStageLength,
                    paramConfig.pRevealStageLength,
                    paramConfig.dispensationPct,
                    paramConfig.pDispensationPct,
                    paramConfig.voteQuorum,
                    paramConfig.pVoteQuorum,
                ],
                config.name,
                operator,
            );
        } else {
            registryReceipt = await registryFactory.newRegistryBYOToken(
                config.token.address,
                [
                    toBN(paramConfig.minDeposit, decimals),
                    toBN(paramConfig.pMinDeposit, decimals),
                    paramConfig.applyStageLength,
                    paramConfig.pApplyStageLength,
                    paramConfig.commitStageLength,
                    paramConfig.pCommitStageLength,
                    paramConfig.revealStageLength,
                    paramConfig.pRevealStageLength,
                    paramConfig.dispensationPct,
                    paramConfig.pDispensationPct,
                    paramConfig.voteQuorum,
                    paramConfig.pVoteQuorum,
                ],
                config.name,
                operator,
            );
        }

        const {
            token,
            plcr,
            parameterizer,
            registry,
        } = registryReceipt.logs[0].args;

        console.log('\n');
        console.log('token:', token);
        console.log('voting:', plcr);
        console.log('parameterizer', parameterizer);
        console.log('registry:', registry);
        console.log('\n');

        return true;
    }

    deployRegistry().then(() => callback());
}