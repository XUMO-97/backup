import binascii
from binascii import b2a_hex, a2b_hex
import csv
import json
import os
import sys, getopt
from time import time
import time
import xlrd
from collections import namedtuple
import time
import unittest
from ontology.smart_contract.native_contract.asset import Asset
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.neo_vm import NeoVm
import requests
import re
import random
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from multiprocess import *

rpc_address = "http://127.0.0.1:20336"
# rpc_address = "http://polaris3.ont.io:20336"
# rpc_address = "http://139.219.139.170:20336"
# rpc_address = "http://dappnode1.ont.io:20336"
sdk = OntologySdk()
sdk.set_rpc((rpc_address))
from datetime import datetime

luckyMoonContractAddress = "794140424d3483dbc3f8aa12d7e2ce78d7e3fa25"

contract_address_str = luckyMoonContractAddress
contract_address_bytearray = bytearray.fromhex(contract_address_str)
contract_address = contract_address_bytearray
contract_address.reverse()

wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
wallet_path1 = "D:\\SmartX_accounts\\Cyano Wallet\\lucknumberAccount\\wallet1.dat"
wallet_path10000 = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet10000.dat"

sdk.wallet_manager.open_wallet(wallet_path)


admin_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
admin_pwd = "xinhao"
pwd = admin_pwd
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)



class TestAsset(unittest.TestCase):

    def test_check_hash(self):
        hash = "e94e67dea2f20ec5c9243a9e050ad3ffcb4166378c4df8a0c33a3c0f56a6654e"
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("Check-res is ", res)
        return True

    def test_testAddress(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("testAddress".encode())
        param_list1 = []
        param_list.append(param_list1)
        # print("***** getExplodePoint", param_list)
        res = self.test_invokeRead(payerAcct, param_list)
        print("res === testAddress", res)
        account = Address(binascii.a2b_hex(res))
        account = account.b58encode()
        print("res === testAddress", account)


    def test_init(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("init", "",param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 20000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("init-res is ", res)
        events = res["Notify"]
        notifyContents = []
        for event in events:
            notifyContent = []
            if event["ContractAddress"] == luckyMoonContractAddress:
                first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                notifyContent.append(first)
                if first == "setRate":
                    num = event["States"][1]
                    if not num:
                        num = "0"
                    num = bytearray.fromhex(num)
                    num.reverse()
                    num = int(num.hex(), 16)
                    notifyContent.append(num)
                    num = event["States"][2]
                    if not num:
                        num = "0"
                    num = bytearray.fromhex(num)
                    num.reverse()
                    num = int(num.hex(), 16)
                    notifyContent.append(num)
                elif first == "setReferralBonus":
                    num = event["States"][1]
                    if not num:
                        num = "0"
                    num = bytearray.fromhex(num)
                    num.reverse()
                    num = int(num.hex(), 16)
                    notifyContent.append(num)
                notifyContents.append(notifyContent)
        print("init-res-event is : ", notifyContents)
        return True

    def test_setOddsTable(self):
        payerAcct = adminAcct

        data = xlrd.open_workbook('D:\\skyinglyh-git\\onchain-work-git\\temporary-Moon\\dataTest.xlsx')
        table = data.sheets()[0]
        nrows = table.nrows
        List = []
        for row in range(0, nrows):
            List1 = []
            cell = table.row(row)[0].value
            List1.append(row + 1)
            List1.append(int(cell * 100))
            List.append(List1)
        param_list = []
        param_list.append("setOddsTable".encode())
        param_list1 = []
        param_list.append([List])



        # param_list = []
        # param_list.append("setOddsTable".encode())
        # param_list1 = []
        # for i in range(1000):
        #     param_list2 = []
        #     param_list2.append(i+1)
        #     param_list2.append(i * 10 + 100)
        #     param_list1.append(param_list2)
        # param_list.append([param_list1])

        print("***** setOddsTable", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === setOddsTable", hash)
        time.sleep(6)
        self.test_handleEvent("setOddsTable", hash)
        return True


    def test_setLuckyToOngRate(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("setLuckyToOngRate".encode())
        param_list1 = []
        param_list1.append(2)
        param_list1.append(1)
        param_list.append(param_list1)
        print("***** setOddsTable", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === setOddsTable", hash)
        time.sleep(6)
        self.test_handleEvent("setLuckyToOngRate", hash)
        return True
    def test_startNewRound(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("startNewRound".encode())
        param_list1 = []
        param_list1.append(1000)
        param_list1.append(89)
        param_list.append(param_list1)
        print("***** startNewRound", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === setOddsTable", hash)
        time.sleep(6)
        self.test_handleEvent("startNewRound", hash)
        return True
    def test_bet(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("bet".encode())
        param_list1 = []
        param_list1.append(payerAcct.get_address().to_array())
        param_list1.append(100)
        param_list.append(param_list1)
        print("***** bet", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === bet", hash)
        time.sleep(6)
        self.test_handleEvent("bet", hash)
        return True
    def test_endCurrentRound(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("endCurrentRound".encode())
        param_list1 = []
        param_list1.append(1000)
        param_list1.append(89)
        param_list2 = []
        param_list3 = []
        param_list3.append(payerAcct.get_address().to_array())
        param_list3.append(100)
        param_list2.append(param_list3)
        param_list1.append(param_list2)
        param_list.append(param_list1)
        # params = BuildParams.create_code_params_script(param_list)
        print("***** endCurrentRound", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === endCurrentRound", hash)
        time.sleep(6)
        self.test_handleEvent("endCurrentRound", hash)
        return True
    def test_getExplodePoint(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("getExplodePoint".encode())
        param_list1 = []
        param_list.append(param_list1)
        # print("***** getExplodePoint", param_list)
        res = self.test_invokeRead(payerAcct, param_list)
        num = bytearray.fromhex(res)
        num.reverse()
        explodePoint = int(num.hex(), 16)
        print("res === getExplodePoint", explodePoint)
        return True

    def test_getRoundExplodePoint(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("getRoundExplodePoint".encode())
        param_list1 = []
        param_list1.append(1)
        param_list.append(param_list1)
        # print("***** getExplodePoint", param_list)
        res = self.test_invokeRead(payerAcct, param_list)
        if res:
            num = bytearray.fromhex(res)
            num.reverse()
            explodePoint = int(num.hex(), 16)
        else:
            explodePoint = "Not Exist"
        print("res === getRoundExplodePoint ===", explodePoint)

        return True

    def test_Test(self):
        print(bytearray.fromhex("e40315e22fc30b4648e3546d33927317f7175dc4c866ea443077798240c5e016"))
        print()






    def test_transferONG(self, fromAcct, toAcct, ongAmount):

        fromAddr = fromAcct.get_address_base58()
        toAddr = toAcct.get_address_base58()
        asset = "ong"
        ass = Asset(sdk)
        payerAddr = fromAddr
        gaslimit = 20000000
        gasprice = 500
        tx = ass.new_transfer_transaction(asset, fromAddr, toAddr, ongAmount, payerAddr, gaslimit, gasprice)
        sdk.sign_transaction(tx, fromAcct)
        hash = sdk.rpc.send_raw_transaction(tx)



    def test_invoke(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)
        #
        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        gaslimit = 20000000
        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:
                hash = sdk.rpc.send_raw_transaction(tx)
            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        print("hash is", hash)
        return hash

    def test_invokeRead(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        sdk.sign_transaction(tx, payerAcct)
        res, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res




    def test_handleEvent(self, action, hash):
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        if action == "setOddsTable":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyMoonContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    notifyContents.append(notifyContent)
            print("setOddsTable-res-events is : ", notifyContents)
        elif action == "setLuckyToOngRate":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyMoonContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "setRate":
                        num = event["States"][1]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                        num = event["States"][2]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("setLuckyToOngRate-res-events is : ", notifyContents)
        elif action == "startNewRound":
            events = res["Notify"]
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyMoonContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "startNewRound":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        timeStamp = str(event["States"][2])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)

                        hashHexString = str(event["States"][3])
                        notifyContent.append(hashHexString)
                    notifyContents.append(notifyContent)
            print("startNewRound-res-events is : ", notifyContents)
        elif action == "bet":
            events = res["Notify"]
            notifyContents = []
            i = 1
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyMoonContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "bet":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        account = Address(binascii.a2b_hex(event["States"][2]))
                        account = account.b58encode()
                        notifyContent.append(account)

                        num = event["States"][3]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("bet-res-events is : ", notifyContents)
        elif action == "endCurrentRound":
            res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
            print("endCurrentRound-res is ", res)
            events = res["Notify"]
            notifyContents = []
            i = 1
            # print("events === ", events)
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == luckyMoonContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    if first == "endCurrentRound":
                        notifyContent.append(first)
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        explodePoint = event["States"][2]
                        if not explodePoint:
                            explodePoint = "0"
                        explodePoint = bytearray.fromhex(explodePoint)
                        explodePoint.reverse()
                        explodePoint = int(explodePoint.hex(), 16)
                        notifyContent.append(explodePoint)

                        salt = event["States"][3]
                        if not salt:
                            salt = "0"
                        salt = bytearray.fromhex(salt)
                        salt.reverse()
                        salt = int(salt.hex(), 16)
                        notifyContent.append(salt)

                        effectiveEscapeAcctPointOddsProfitList = event["States"][4]
                        notify1 = []
                        for effectiveEscapeAcctPointOddsProfit in effectiveEscapeAcctPointOddsProfitList:
                            notify2 = []
                            account = Address(binascii.a2b_hex(effectiveEscapeAcctPointOddsProfit[0]))
                            account = account.b58encode()
                            notify2.append(account)

                            escapePoint = effectiveEscapeAcctPointOddsProfit[1]
                            if not escapePoint:
                                escapePoint = "0"
                            escapePoint = bytearray.fromhex(escapePoint)
                            escapePoint.reverse()
                            escapePoint = int(escapePoint.hex(), 16)
                            notify2.append(escapePoint)

                            # odds = effectiveEscapeAcctPointOddsProfit[2]
                            # if not odds:
                            #     odds = "0"
                            # odds = bytearray.fromhex(odds)
                            # odds.reverse()
                            # odds = int(odds.hex(), 16)
                            # notify2.append(odds)

                            profit = effectiveEscapeAcctPointOddsProfit[2]
                            if not profit:
                                profit = "0"
                            profit = bytearray.fromhex(profit)
                            profit.reverse()
                            profit = int(profit.hex(), 16)
                            notify2.append(profit)

                            notify1.append(notify2)

                        notifyContent.append(notify1)
                        # print("endCurrentRound-res-event is : ", notifyContent)
                    elif first == "Error":
                        errorCode = event["States"][1]
                        if not errorCode:
                            errorCode = "0"
                        errorCode = bytearray.fromhex(errorCode)
                        errorCode.reverse()
                        errorCode = int(errorCode.hex(), 16)
                        notifyContent.append(errorCode)
                    notifyContents.append(notifyContent)
            print("endCurrentRound-res-events is : ", notifyContents)

        return True
