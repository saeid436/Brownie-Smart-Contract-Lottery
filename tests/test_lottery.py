from brownie import Lottery, accounts, network, config
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
    config['networks'][network.show_active()]['eth_usd_price_feed'],
    {'from':account},
    )

    usdToETH = lottery.getEntranceFee()
    assert usdToETH > Web3.toWei(0.014, 'ether')
    assert usdToETH < Web3.toWei(0.018, 'ether')
