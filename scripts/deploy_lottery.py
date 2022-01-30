import imp
from brownie import Lottery, network, config, accounts
from scripts.helpful_scripts import getAccount, getContract




def deploy_lottery():
    account = getAccount()
    lottery = Lottery.deploy(
        getContract('eth_usd_price_feed').address
    )




def main():
    deploy_lottery()
