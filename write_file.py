import json
import time
import datetime

def timestamp():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

def write_file(pairs):
    try:
        print(f"{timestamp()} Write pairs to file {len(pairs)} pairs")
        filename = f"./pairs/pairs-{int(time.time() * 1000)}.json"
        with open(filename, 'w') as f:
            json.dump(pairs, f)
        return
    except Exception as e:
        print(e)
        raise e
