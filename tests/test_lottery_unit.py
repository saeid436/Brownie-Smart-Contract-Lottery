from cgitb import lookup
from brownie import Lottery, accounts, network, config, exceptions
import pytest
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, getAccount, fund_with_link, getContract

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
     
    # Arrrange:
    lottery = deploy_lottery()
    # Act:
    # 2600 eth/usdt
    # usdEntryFee is 50
    # 2500/1 == 50/x == 0.02
    expectedEntranceFee = Web3.toWei(0.025, 'ether')
    enteranceFee = lottery.getEntranceFee()
    # Assert:
    assert expectedEntranceFee == enteranceFee

def test_cant_enter_unless_started():
    # Arrange:
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Act / Assert:
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from':getAccount(), 'value': lottery.getEntranceFee()})
    
def test_can_start_and_test_lottery():
    # Arrange:
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    lottery.startLottery({'from':account})
    # Act:
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    # Asssert:
    assert lottery.players(0) == account

def test_can_end_lottery():
    # Arrange:
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    lottery.startLottery({'from':account})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    # Act:
    fund_with_link(lottery)
    lottery.endLottery({'from':account})
    # Assert:
    assert lottery.lotteryState() == 2

def test_can_pick_winner_correctly():
     # Arrange:
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    lottery.startLottery({'from':account})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    lottery.enter({'from':getAccount(_index=1), 'value':lottery.getEntranceFee()})
    lottery.enter({'from':getAccount(_index=2), 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({'from':account})
    request_id = transaction.events['RequestRandomness']['requestId']
    STATIC_RNG = 666
    getContract('vrf_coordinator').callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address,
        {'from':account}
        )
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # Winner -> 666 % 3 => 0 => account[0] is winner!!
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
