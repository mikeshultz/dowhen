from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal
from dowhen.common import same_day, same_hour, same_minute
from dowhen.common.logger import get_logger

log = get_logger(__name__)

_LAST_TRIGGERED_DT = dict()


def clear_metrics():
    """ Clears all metrics """
    global _LAST_TRIGGERED_DT
    _LAST_TRIGGERED_DT = dict()


def now_is_same(interval):
    """ Check if the last triggered datetime of an interval is the same day as
    today """

    same = False
    now = datetime.now(tz=tzlocal())

    if interval == 'daily':
        same = same_day(_LAST_TRIGGERED_DT.get(interval), now)
    elif interval == 'hourly':
        same = same_hour(_LAST_TRIGGERED_DT.get(interval), now)
    elif interval == 'minutely':
        same = same_minute(_LAST_TRIGGERED_DT.get(interval), now)

    return same


def _interval_trigger(interval):
    """ Generic trigger for datetime intervals """
    if now_is_same(interval):
        return None
    _LAST_TRIGGERED_DT[interval] = datetime.now(tz=tzlocal())
    return _LAST_TRIGGERED_DT[interval]


def daily():
    """ Triggers every day """
    return _interval_trigger('daily')


def hourly():
    """ Triggers every hour """
    return _interval_trigger('hourly')


def minutely():
    """ Triggers every miniute """
    return _interval_trigger('minutely')


def time(when):
    """ Triggers when the time matches t """
    dt = parse(when).replace(tzinfo=tzlocal())
    now = datetime.now(tz=tzlocal())
    key = 'time-{}:{}:{}'.format(dt.hour, dt.minute, dt.second)

    if now < dt:
        log.debug('{} is in the future.'.format(dt))
        return None

    if same_day(_LAST_TRIGGERED_DT.get(key), now):
        log.debug('datetime.time already fired today (@ {}).'.format(
            _LAST_TRIGGERED_DT.get(key)
        ))
        return None

    _LAST_TRIGGERED_DT[key] = now

    return dt


CATALOG = {
    'daily': {
        'name': 'Daily',
        'description': daily.__doc__,
        'func': daily,
    },
    'hourly': {
        'name': 'Hourly',
        'description': hourly.__doc__,
        'func': hourly,
    },
    'minutely': {
        'name': 'Minutely',
        'description': minutely.__doc__,
        'func': minutely,
    },
    'time': {
        'name': 'Time',
        'description': time.__doc__,
        'func': time,
    },
}
