from datetime import datetime, timedelta
from functools import wraps

from dateutil import tz
from dateutil.parser import parse
from flask import session, redirect, url_for
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


def check_due(issue_date_str, return_date_str, days):
    issue_date = parse(issue_date_str).replace(tzinfo=tz.gettz(DUBLIN_TIMEZONE))
    return_date = parse(return_date_str).replace(tzinfo=tz.gettz(DUBLIN_TIMEZONE))
    used_days = get_days_between_timestamp(issue_date, datetime.now(timezone(DUBLIN_TIMEZONE)))

    days_diff = used_days - days
    return max(days_diff, 0)


def get_days_between_timestamp(timestamp1, timestamp2):
    duration = timestamp2 - timestamp1
    return duration.days


def check_or_raise(var, expected, msg):
    if var != expected:
        raise LibraryException(msg, "IVD_OPN", 400)


def getWildCardWords(var):
    return "%" + str(var) + "%"


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('user.user_login'))

    return wrapped_view


def checkUniqueAndThrow(error_message):
    duplicates = []
    if "duplicate key value violates unique constraint" in error_message:
        if "username" in error_message:
            duplicates.append("Username")
        if "email" in error_message:
            duplicates.append("Email")
        if "contact" in error_message:
            duplicates.append("Contact")

        if duplicates:
            fields_str = ', '.join(duplicates)
            raise LibraryException(
                f"{fields_str} already exist. Please choose different values for {fields_str.lower()}.",
                error_code="ALD_EXISTS", http_status=400)
