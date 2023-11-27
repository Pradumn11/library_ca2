from datetime import datetime, timedelta
from pytz import timezone
from src.exceptions.LibraryException import LibraryException

DUBLIN_TIMEZONE = "Europe/Dublin"


def check_row_change(num):
    if num == 0:
        raise LibraryException("Something Went Wrong", "SWR_BOOK", 500)


def check_book_availability(availability):
    if availability <= 0:
        raise LibraryException("Insufficient Quantity", "IVD_BOOK", 400)


def check_user_book_issued(issued: int):
    if issued >= 3:
        raise LibraryException("Already Issued 3 Books", "3ALD_BOOK", 400)


def get_current_timestamp(timezone_str: str):
    return datetime.now(timezone(timezone_str)).replace(microsecond=0).isoformat()


def get_return_time(days, timezone_str):
    return (datetime.now(timezone(timezone_str)) + timedelta(days=days)).replace(microsecond=0).isoformat()


def get_formatted_time(timestamp_str):
    timestamp = datetime.fromisoformat(timestamp_str)
    return timestamp.strftime("%d %B %Y, %I:%M %p")


def check_due(issue_date_str, return_date_str):
    issue_date = datetime.fromisoformat(issue_date_str)
    return_date = datetime.fromisoformat(return_date_str) if return_date_str else None

    issued_days = get_days_between_timestamp(issue_date, return_date)
    used_days = get_days_between_timestamp(issue_date, datetime.now(timezone(DUBLIN_TIMEZONE)))

    days_diff = used_days - issued_days
    return max(days_diff, 0) + 1


def get_days_between_timestamp(timestamp1, timestamp2):
    duration = timestamp2 - timestamp1
    return duration.days


def check_or_raise(var, expected, msg):
    if var != expected:
        raise LibraryException(msg, "IVD_OPN", 400)
