from tronapi import Tron, HttpProvider
from solc import compile_source
import unittest

full_node = HttpProvider('https://api.shasta.trongrid.io')
solidity_node = HttpProvider('https://api.shasta.trongrid.io')
event_server = HttpProvider('https://api.shasta.trongrid.io')
private_key = '3fb598ba9521c34b5d626f9d4c353baf9663e1f4853c13ff717aa54f19c7c47d'

tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.4;

library ConvertLib{
	function convert(uint amount,uint conversionRate) public pure returns (uint convertedAmount)
	{
		return amount * conversionRate;
	}
}

contract MetaCoin {
	mapping (address => uint) balances;

	event Transfer(address _from, address _to, uint256 _value);

	constructor() public {
		balances[tx.origin] = 10000;
	}

	function sendCoin(address receiver, uint amount) public returns(bool sufficient) {
		if (balances[msg.sender] < amount) return false;
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		emit Transfer(msg.sender, receiver, amount);
		return true;
	}

	function getBalanceInEth(address addr) public view returns(uint){
		return ConvertLib.convert(getBalance(addr),2);
	}

	function getBalance(address addr) public view returns(uint) {
		return balances[addr];
	}
}

'''


class Test(unittest.TestCase):

    def test_deployContract(self):
        compiled_sol = compile_source(contract_source_code)
        contract_interface = compiled_sol['<stdin>:MetaCoin']

        MetaCoin = tron.trx.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']
        )

        # Submit the transaction that deploys the contract
        tx_data = MetaCoin.deploy(
            fee_limit=10 ** 9,
            call_value=0,
            consume_user_resource_percent=1
        )

        sign = tron.trx.sign(tx_data)
        result = tron.trx.broadcast(sign)
        print(result)


if __name__ == '__main__':
    unittest.main()
