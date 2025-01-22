from datetime import datetime

def is_expired(date_time: datetime) -> bool:
    now = datetime.now()
    diff = now - date_time
    # if it is more or equal to 24 hours, it is expired
    return diff.seconds / 3600 >= 24

def string_to_datetime(date_time: str) -> datetime:
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_time, date_format)