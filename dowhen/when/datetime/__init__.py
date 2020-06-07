from datetime import datetime
from dateutil.parser import parse
from dowhen.common import same_day, same_hour, same_minute
from dowhen.common.logger import get_logger

log = get_logger(__name__)

_LAST_TRIGGERED_DT = {}


def now_is_same(interval):
    now = datetime.now()

    same = False

    if interval == 'daily':
        same = same_day(_LAST_TRIGGERED_DT.get('daily'), now)
    elif interval == 'hourly':
        same = same_hour(_LAST_TRIGGERED_DT.get('daily'), now)
    elif interval == 'minutely':
        same = same_minute(_LAST_TRIGGERED_DT.get('daily'), now)

    if same:
        return True

    return False


def daily():
    """ Triggers every day """
    if not now_is_same('daily'):
        return None
    return datetime.now()


def hourly():
    """ Triggers every hour """
    if not now_is_same('hourly'):
        return None
    return datetime.now()


def minutely():
    """ Triggers every miniute """
    if not now_is_same('minutely'):
        return None
    return datetime.now()


def time(when):
    """ Triggers when the time matches t """
    dt = parse(when)
    now = datetime.now()
    key = 'time-{}:{}:{}'.format(dt.hour, dt.minute, dt.second)

    if dt > now:
        log.debug('{} is in the future.'.format(dt))
        return None

    if same_day(_LAST_TRIGGERED_DT.get(key), now):
        log.debug('datetime.time already fired today (@ {}).'.format(
            _LAST_TRIGGERED_DT[key]
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
