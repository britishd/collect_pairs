from dotenv import load_dotenv
load_dotenv()

import os
import time
import asyncio
import psutil
import schedule
import time
import datetime

def timestamp():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

def check_memory_consumption():
    """Function to check memory consumption and print it in MB"""
    memory_usage = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"{timestamp()} Memory usage: {memory_usage:.2f} MB")

# Schedule the function to run every 30 seconds
check_memory_consumption()
#schedule.every(30).seconds.do(check_memory_consumption)


from write_file import write_file
from generate_chunks import generate_chunks
from uniswap_factory_abi import factory_abi
from get_pairs_length import get_pairs_length
from check_args import check_params
from request_pair_data import request_data

PROVIDER = os.getenv('PROVIDER')
PROTOCOL = os.getenv('PROTOCOL')
FACTORY = os.getenv('FACTORY')
AMOUNT = os.getenv('AMOUNT')
SKIP = os.getenv('SLIP')
MAX_CHUNKS = os.getenv('MAX_CHUNKS')
PAIRS_PER_FILE = os.getenv('PAIRS_PER_FILE')


def main(provider, protocol, factory_address, amount, skip=0):
    check_params(provider, protocol, factory_address, amount)

    skip = int(skip)
    amount = int(amount)
    maxChunk = int(MAX_CHUNKS)
    pairsPerFile = int(PAIRS_PER_FILE)
    

    pairsLen = get_pairs_length(
        provider,
        factory_abi,
        factory_address
    )

    if pairsLen <= 0:
        raise ValueError('No pairs in factory')
    
    if isinstance(pairsLen, str):
        pairsLen = int(pairsLen)

    pairsLen = pairsLen - 1;

    if pairsPerFile >= pairsLen:
        pairsPerFile = pairsLen

    if amount >= pairsLen:
        amount = pairsLen;

    if (amount < maxChunk):
        maxChunk = amount

    amount = amount if amount else pairsLen
    # TODO: env file can not be soruce of truth....
    maxPairsCount = amount // maxChunk if amount > maxChunk else 1
    iterablePairsLen = pairsLen - skip

    # TODO: index can be 0 but we do not include it
    chunks = generate_chunks(amount, maxChunk, iterablePairsLen)
    pairs = []

    for chunk in chunks:
        if maxPairsCount < 0:
            break
        try:

            time.sleep(2)
            print(f"{timestamp()} request data")
            data = request_data(provider, factory_abi, factory_address, chunk)
            pairs.extend(data)
            print(f"{timestamp()} I have {len(pairs)} pairs")

            # if len(pairs) >= pairsPerFile:
            #     write_file(pairs)
            #     pairs = []

            check_memory_consumption()
        except Exception as e:
            print(e)

        maxPairsCount -= 1

    write_file(pairs)

main(PROVIDER, PROTOCOL, FACTORY, AMOUNT)
print('Finish');
