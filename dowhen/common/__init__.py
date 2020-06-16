import re
from datetime import date, datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal

MAC_STANDARD_PATTERN = r'^[0-9A-F]{2}\:[0-9A-F]{2}\:[0-9A-F]{2}\:[0-9A-F]{2}\:[0-9A-F]{2}\:[0-9A-F]{2}$'
MAC_WEMO_PATTERN = r'^[0-9A-F]{12}$'


def getint(d, k, default=None):
    if type(d) != dict:
        raise ValueError('d is not a dict')

    if k in d:
        return int(d[k])

    return default


def normalize_mac_address(mac):
    assert type(mac) == str, "Invalid mac type: {}".format(type(mac))
    if re.match(MAC_STANDARD_PATTERN, mac):
        return mac
    elif re.match(MAC_WEMO_PATTERN, mac):
        parts = []
        for i in range(0, 12):
            if i > 0 and i % 2 == 0:
                parts.append(':')
            parts.append(mac[i])
        return ''.join(parts)
    else:
        raise ValueError("Unknown mac address format")


def same_day(a, b):
    """ Check if both datetimes are on the same day """

    if type(a) not in (datetime, date) or type(b) not in (datetime, date):
        return False

    return (
        a.year == b.year
        and a.month == b.month
        and a.day == b.day
    )


def same_hour(a, b):
    """ Check if both datetimes are on the same hour of the same day """

    if type(a) != datetime or type(b) != datetime:
        return False

    return (
        a.year == b.year
        and a.month == b.month
        and a.day == b.day
        and a.hour == b.hour
    )


def same_minute(a, b):
    """ Check if both datetimes are on the same minute of the same hour of the
    same day """

    if type(a) != datetime or type(b) != datetime:
        return False

    return (
        a.year == b.year
        and a.month == b.month
        and a.day == b.day
        and a.hour == b.hour
        and a.minute == b.minute
    )


def any_in_any(a, b):
    """ Check if any elements in a are in b """
    for x in a:
        if x in b:
            return True
    return False


def local_now():
    """ Get the current date and time in the local timezone """
    return datetime.now(tz=tzlocal())


def local_time_parse(ts):
    """ Parse a time string using the local timezone """
    dt = parse(ts)

    # If not timezone was in the string, use the local timezone
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tzlocal())

    return dt
