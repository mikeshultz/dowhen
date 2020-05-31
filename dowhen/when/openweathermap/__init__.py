from datetime import datetime, timedelta

from dowhen.common import same_day
from dowhen.common.logger import get_logger
from dowhen.when.openweathermap.owmapi import get_forecast

log = get_logger(__name__)

_LAST_TRIGGERED_DATE = {}


def sunrise(zip):
    """ When the sun is up """
    global _LAST_TRIGGERED_DATE

    now = datetime.now()
    forecast = get_forecast(zip=zip)

    if not forecast.get('city') or not forecast['city'].get('sunrise'):
        log.error('Unable to get sunrise from forecast for zip: {}'.format(
            zip
        ))
        return False

    # Only trigger this once per day
    if same_day(_LAST_TRIGGERED_DATE.get('sunrise'), now):
        return False

    _LAST_TRIGGERED_DATE['sunrise'] = now

    return datetime.fromtimestamp(forecast['city']['sunrise']) <= now


def sunset(zip):
    """ When the sun is down """
    global _LAST_TRIGGERED_DATE

    now = datetime.now()
    forecast = get_forecast(zip=zip)

    if not forecast.get('city') or not forecast['city'].get('sunset'):
        log.error('Unable to get sunset from forecast for zip: {}'.format(
            zip
        ))
        return False

    # Only trigger this once per day
    if same_day(_LAST_TRIGGERED_DATE.get('sunset'), now):
        return False

    _LAST_TRIGGERED_DATE['sunset'] = now

    return (
        datetime.fromtimestamp(forecast['city']['sunset']) <= now
        or datetime.fromtimestamp(forecast['city']['sunrise']) >= now
    )


def precipitating(zip):
    """ If it is currently precipitating """
    raise NotImplementedError('precipitating not implemented')


CATALOG = {
    'sunrise': {
        'name': 'Sunrise',
        'description': sunrise.__doc__,
        'func': sunrise,
    },
    'sunset': {
        'name': 'Sunset',
        'description': sunset.__doc__,
        'func': sunset,
    },
    'precipitating': {
        'name': 'Precipitating',
        'description': precipitating.__doc__,
        'func': precipitating,
    },
}
