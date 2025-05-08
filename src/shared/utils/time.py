import time
import random
import datetime

def now_timestamp() -> int:
    return int(round(time.time()))

def now_timestamp_milli() -> int:
    return int(round(time.time() * 1000))

def datetime_to_timestamp(datetime: datetime.datetime) -> int:
    return int(time.mktime(datetime.timetuple()))

def sleep_random_float(min: float = 0.5, max: float = 3):
    time.sleep(round(random.uniform(min, max), 1))