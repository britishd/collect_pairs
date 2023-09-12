
from web3 import Web3
from factory import FactoryContract


def get_pairs_length(provider, abi, address):
    try:
        web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
        factory = FactoryContract(abi, address, web3)
        length = factory.get_pairs_length()
        return length
    except Exception as e:
        print(e)
        return None

