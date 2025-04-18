import time
import datetime

def now_timestamp() -> int:
    return int(round(time.time()))

def now_timestamp_milli() -> int:
    return int(round(time.time() * 1000))

def datetime_to_timestamp(datetime: datetime.datetime) -> int:
    return int(time.mktime(datetime.timetuple()))