import concurrent.futures

from web3 import Web3
from factory import FactoryContract
from uniswap_pair_abi import uniswap_pair_abi
from erc20_abi import erc20_abi

def request_data(provider, factory_abi, factory_address, pair_indexes):
    try:
        web3 = Web3(Web3.HTTPProvider(provider, request_kwargs={'timeout': 60}))
        factory = FactoryContract(factory_abi, factory_address, web3)

        pairs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(pair_indexes)) as executor:
            future_to_url = (executor.submit(get_pair_data, index, factory_abi, factory, web3) for index in pair_indexes)
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    pairs.append(data)
        return [pair for pair in pairs if pair is not None]

    except Exception as e:
        print("here: ", e)


def get_pair_data(index, abi, factory, web3):
    pair = factory.get_pairs(index)

    if not pair:
        return None

    token0, token1 = get_tokens_address(pair, abi, web3)

    if not token0 or not token1:
        return None

    token0_decimal, token0_symbol = get_token_data(token0, web3)
    token1_decimal, token1_symbol = get_token_data(token1, web3)

    return {
        "token0": {
            "address": token0,
            "decimals": token0_decimal or '',
            "symbols": token0_symbol or ''
        },
        "token1": {
            "address": token1,
            "decimals": token1_decimal or '',
            "symbols": token1_symbol or ''
        },
        "pair": f"{token0_symbol or 'Symbol not exist'}-{token1_symbol or 'Symbol not exist'}",
        "pairAddress": pair,
        "index": index
    }


def get_tokens_address(pair, abi, web3):
    contract = web3.eth.contract(address=pair, abi=uniswap_pair_abi)

    token0 = ''
    token1 = ''

    try:
        token0 = contract.functions.token0().call()
    except Exception as e:
        print("token0: ", e)

    try:
        token1 = contract.functions.token1().call()
    except Exception as e:
        print("token1: ", e)

    return (token0, token1)


def get_token_data(token, web3):
    contract = web3.eth.contract(address=token, abi=erc20_abi)

    decimal = ''
    symbol = ''

    try:
        decimal = contract.functions.decimals().call()
    except Exception as e:
        pass

    try:
        symbol = contract.functions.symbol().call()
    except Exception as e:
        pass

    return (decimal, symbol)
