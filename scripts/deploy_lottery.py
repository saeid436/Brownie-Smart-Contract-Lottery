import imp
from brownie import Lottery, network, config, accounts
from scripts.helpful_scripts import getAccount, getContract, fund_with_link
import time



def deploy_lottery():
    account = getAccount()
    lottery = Lottery.deploy(
        getContract('eth_usd_price_feed').address,
        getContract('vrf_coordinator').address,
        getContract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyhash'],
        {'from':account},
        publish_source = config['networks'][network.show_active()].get('verify', False),

    )

    print('Deployed Lottery!!')
    return lottery

def start_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    startingTx = lottery.startLottery({'from':account})
    startingTx.wait(1)
    print('Lottery is started!!!')

def enter_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({'from':account, 'value':value})
    tx.wait(1)
    print('You entered the lottery!!!')

def end_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    endingTransaction = lottery.endLottery({'from':account})
    endingTransaction.wait(1)
    time.sleep(60)
    print(f'{lottery.recentWinner()} is the new winner!!' )
    
def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
