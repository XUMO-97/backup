/* eslint-env mocha */
/* global assert contract */
const fs = require('fs')

const config = JSON.parse(fs.readFileSync('./conf/config.json'))
const paramConfig = config.paramDefaults

const utils = require('../utils.js')

contract('Registry', (accounts) => {
  describe('Function: getData', () => {
    const [applicant] = accounts

    let token, registry

    before(async () => {
      const { registryProxy, tokenInstance } = await utils.getProxies()
      registry = registryProxy
      token = tokenInstance

      await utils.approveProxies(accounts, token, false, false, registry)
    });

    it('should return false if the listing does not exist', async () => {
      const listing = utils.getListingHash('tcsm')
      const [exists, data] = await registry.getData.call(listing)
      assert.strictEqual(exists, false)
      assert.strictEqual(data, '')
    })

    it('should return false if the listing is pending', async () => {
      const listing = utils.getListingHash('tcsm1')
      await utils.as(applicant, registry.apply, listing, paramConfig.minDeposit, "test")
      const [exists, data] = await registry.getData.call(listing)
      assert.strictEqual(exists, false)
      assert.strictEqual(data, '')
    })

    it('should return the correct data for a whitelisted listing', async () => {
      const listing = utils.getListingHash('tcsm2')
      await utils.addToWhitelistWithData(listing, paramConfig.minDeposit, "test", applicant, registry)
      const [exists, data] = await registry.getData.call(listing)
      assert.strictEqual(exists, true)
      assert.strictEqual(data, 'test')
    })
  })
})
