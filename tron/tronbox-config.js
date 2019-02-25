module.exports = {
    networks: {
        // development: {
        //   from: 'TMziYNE4MnUginjPzr92pZkCiZ3ovYPEJf',
        //   privateKey: 'd2919b402a64172a9ae637c99ccd264ecb11e5935fb5c23b7b76d9923a9faf2a',
        //   consume_user_resource_percent: 30,
        //   fee_limit: 100000000,
        //   fullNode: "https://api.trongrid.io:8090",
        //   solidityNode: "https://api.trongrid.io:8091",
        //   eventServer: "https://api.trongrid.io",
        //   network_id: "2" // Match any network id
        // },
        shasta: {
        from: 'TMziYNE4MnUginjPzr92pZkCiZ3ovYPEJf',
        privateKey: 'd2919b402a64172a9ae637c99ccd264ecb11e5935fb5c23b7b76d9923a9faf2a',
        userFeePercentage: 50,
        feeLimit: 1e8,
        fullHost: "https://api.shasta.trongrid.io",
        solidityNode: "https://api.shasta.trongrid.io",
        eventServer: "https://api.shasta.trongrid.io",
        network_id: "2"
        },
        // mainnet: {
        //   // Don't put your private key here:
        //   privateKey: process.env.PRIVATE_KEY_MAINNET,
        //   /*
        //   Create a .env file (it must be gitignored) containing something like
        //     export PRIVATE_KEY_MAINNET=4E7FECCB71207B867C495B51A9758B104B1D4422088A87F4978BE64636656243
        //   Then, run the migration with:
        //     source .env && tronbox migrate --network mainnet
        //   */
        //   userFeePercentage: 100,
        //   feeLimit: 1e8,
        //   fullHost: "https://api.trongrid.io",
        //   network_id: "1"
        // }
    }
};