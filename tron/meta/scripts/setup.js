var fs = require('fs')
var path = require('path')
var MetaCoin = require('../build/contracts/MetaCoin')

const address = MetaCoin.networks['2'].address

console.log('The app has been configured.')
console.log('Run "npm run dev" to start it.')

// const tronboxJs = require('../tronbox').networks.shasta
const metacoinConfig = {
  contractAddress: address,
  privateKey: 'd2919b402a64172a9ae637c99ccd264ecb11e5935fb5c23b7b76d9923a9faf2a',
  fullHost: "https://api.shasta.trongrid.io"
}

fs.writeFileSync(path.resolve(__dirname, '../src/js/metacoin-config.js'),`var metacoinConfig = ${JSON.stringify(metacoinConfig, null, 2)}`)
