import imp
from brownie import accounts, network, config, Contract, MockV3Aggregator, VRFCoordinatorMock, LinkToken, interface
from eth_typing import ContractName

FROKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']

def getAccount(_index=None, _id=None):

    # accounts[0]
    # accounts.add(.env)
    # accounts.load(id)
    if _index:
        return accounts[_index]
    if _id:
        return accounts.load(_id)
    if(
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FROKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    
    return accounts.add(config['wallets']['from_key'])

contractToMock = {'eth_usd_price_feed': MockV3Aggregator,
'vrf_coordinator':VRFCoordinatorMock,
'link_token': LinkToken}

def getContract(_contractName):
    """This contract will grab the contract addresses from the brownie config if defined, otherwise,
    it will deploy a mock version of that contract, and return that mock contract

        Args:
            contract_name(string)

        Return:
            brownie.network.contract.ProjectContract: The most recently version deployed of this contract.
    """
    contractType = contractToMock[_contractName]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contractType) <= 0:
        # MockV3Aggregator.length
            deployMocks()
        contract = contractType[-1]
        # MockV3Aggregator[-1]
    else:
        contractAddress = config['wallets'][network.show_active()][_contractName]
        # Address
        # ABI
        contract = Contract.from_abi(
            contractType._name, contractAddress, contractType.abi
        )
        #MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000

def deployMocks(_decimal=DECIMALS, _initialValue=INITIAL_VALUE):
    account = getAccount()
    MockV3Aggregator.deploy(
        _decimal, _initialValue, {'from':account}
    )
    link_token = LinkToken.deploy({'from':account})
    VRFCoordinatorMock.deploy(link_token.address, {'from':account})
    print('Deployed!')

def fund_with_link(_contractAddress, _account=None, _linkToken = None, _amount = 100000000000000000):  # 0.1 Link
    account = _account if _account else getAccount()
    linkToken = _linkToken if _linkToken else getContract('link_token')
    tx = linkToken.transfer(_contractAddress, _amount, {'from':account})
    #linkTokenContract = interface.LinkTokenInterface(linkToken.address)
    #tx = linkTokenContract.transfer(_contractAddress, _amount, {'from':account})
    tx.wait(1)
    print('Fund the contract!!')
    return tx