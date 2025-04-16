import time

def now_timestamp() -> int:
    return int(round(time.time()))

def now_timestamp_milli() -> int:
    return int(round(time.time() * 1000))