from brownie import Lottery, accounts, network, config
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3

def test_get_entrance_fee():
    # Arrrange:
    lottery = deploy_lottery()
    # Act:
    # 2600 eth/usdt
    # usdEntryFee is 50
    # 2000/1 == 50/x == 0.0192
    expectedEntranceFee = Web3
    enteranceFee = lottery.getEntranceFee()
    # Assert:

