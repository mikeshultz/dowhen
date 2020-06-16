import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal
from unittest.mock import patch
from freezegun import freeze_time

from dowhen.when.datetime import clear_metrics, daily, hourly, minutely, time

from .const import (
    YEAR,
    MONTH,
    DAY,
    ONE_AM,
    ONE_PM,
    TWELVE_FIFTY_NINE_AM,
    TWELVE_FIFTY_NINE_PM,
    FIVE_AM,
    FIVE_PM,
    ONE_DAY,
    ONE_HOUR,
    ONE_MINUTE,
    TEN_SECONDS,
)


def test_datetime_time():
    """ Test the datetime when module's time trigger """

    # 1:00 AM
    time1 = '{}-{}-{} 01:00:00'.format(YEAR, MONTH, DAY)
    time1_dt = parse(time1).replace(tzinfo=tzlocal())

    # One minute before
    with freeze_time(TWELVE_FIFTY_NINE_AM):
        when = time(time1)
        assert(when is None)

    clear_metrics()

    # Same minute
    with freeze_time(ONE_AM):
        when = time(time1)
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == time1_dt)
        assert(when > TWELVE_FIFTY_NINE_AM)

    clear_metrics()

    # After
    with freeze_time(FIVE_AM):
        when = time(time1)
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == time1_dt)
        assert(when < FIVE_AM)


def test_datetime_time_continuity():
    """ Test the datetime when module's time trigger """
    clear_metrics()

    # 1:00 AM
    time1 = '01:00:00'
    time1_dt = parse('{}-{}-{} {}'.format(
        TWELVE_FIFTY_NINE_AM.year,
        TWELVE_FIFTY_NINE_AM.month,
        TWELVE_FIFTY_NINE_AM.day,
        time1
    )).replace(tzinfo=tzlocal())

    # One minute before
    with freeze_time(TWELVE_FIFTY_NINE_AM):
        when = time(time1)
        assert(when is None)

    # Same minute
    with freeze_time(ONE_AM):
        when = time(time1)
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == time1_dt)
        assert(when > TWELVE_FIFTY_NINE_AM)

    # Already triggered, shouldn't trigger again
    with freeze_time(FIVE_AM):
        when = time(time1)
        assert(when is None)

    ####
    # NEXT DAY
    ####

    # One minute before
    with freeze_time(TWELVE_FIFTY_NINE_AM + ONE_DAY):
        when = time(time1)
        assert(when is None)

    # Same minute
    with freeze_time(ONE_AM + ONE_DAY):
        when = time(time1)
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == time1_dt + ONE_DAY)
        assert(when > TWELVE_FIFTY_NINE_AM + ONE_DAY)

    # Already triggered, shouldn't trigger again
    with freeze_time(FIVE_AM + ONE_DAY):
        when = time(time1)
        assert(when is None)


def test_datetime_daily():
    """ Test the datetime daily trigger """
    clear_metrics()

    with freeze_time(TWELVE_FIFTY_NINE_AM):
        when = daily()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == TWELVE_FIFTY_NINE_AM)

    # Already triggered, shouldn't trigger again
    with freeze_time(ONE_AM):
        when = daily()
        assert(when is None)

    # Already triggered, shouldn't trigger again
    with freeze_time(FIVE_AM):
        when = daily()
        assert(when is None)

    ####
    # NEXT DAY
    ####

    with freeze_time(TWELVE_FIFTY_NINE_AM + ONE_DAY):
        when = daily()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == TWELVE_FIFTY_NINE_AM + ONE_DAY)

    # Already triggered, shouldn't trigger again
    with freeze_time(ONE_AM + ONE_DAY):
        when = daily()
        assert(when is None)

    # Already triggered, shouldn't trigger again
    with freeze_time(FIVE_AM + ONE_DAY):
        when = daily()
        assert(when is None)


def test_datetime_hourly():
    """ Test the datetime hourly trigger """
    clear_metrics()

    with freeze_time(TWELVE_FIFTY_NINE_AM - ONE_MINUTE):
        when = hourly()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == TWELVE_FIFTY_NINE_AM - ONE_MINUTE)

    with freeze_time(TWELVE_FIFTY_NINE_AM):
        when = hourly()
        assert(when is None)

    ####
    # NEXT HOUR
    ####

    with freeze_time(ONE_AM):
        when = hourly()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == ONE_AM)

    # Already triggered, shouldn't trigger again
    with freeze_time(ONE_AM + ONE_MINUTE):
        when = hourly()
        assert(when is None)


def test_datetime_minutely():
    """ Test the datetime minutely trigger """
    clear_metrics()

    with freeze_time(ONE_AM):
        when = minutely()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == ONE_AM)

    with freeze_time(ONE_AM + TEN_SECONDS):
        when = minutely()
        assert(when is None)

    with freeze_time(ONE_AM + ONE_MINUTE):
        when = minutely()
        assert(when is not None)
        assert(isinstance(when, datetime.datetime))
        assert(when == ONE_AM + ONE_MINUTE)

    # Already triggered, shouldn't trigger again
    with freeze_time(ONE_AM + ONE_MINUTE):
        when = minutely()
        assert(when is None)
