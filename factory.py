class FactoryContract:
    def __init__(self, abi, address, web3):
        self.web3 = web3

        self.factory_contract = self.web3.eth.contract(abi=abi, address=address)

    def get_pair_address(self, token0, token1):
        try:
            return self.factory_contract.functions.getPair(token0, token1).call()
        except Exception as e:
            print('Factory -> getPairAddress : ', e)
            raise Exception(f"Did not found Pair address for {token0} and {token1}")

    def get_pairs_length(self):
        try:
            value = self.factory_contract.functions.allPairsLength().call()
            return value
        except Exception as e:
            print('Factory -> getPairsLength(): ', e)
            return 0

    def get_pairs(self, pair_index):
        try:
            return self.factory_contract.functions.allPairs(pair_index).call()
        except Exception as e:
            print(f'Factory -> getPairs(): {pair_index} {e} ')
            return None
