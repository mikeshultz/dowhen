from datetime import datetime, timedelta
from dateutil.tz import tzoffset, tzlocal

from dowhen.common import same_day, local_now
from dowhen.common.logger import get_logger
from dowhen.when.openweathermap.owmapi import get_forecast

log = get_logger(__name__)

_LAST_TRIGGERED_DATE = {}


def sunrise(zip):
    """ When the sun is up """
    global _LAST_TRIGGERED_DATE

    key = "sunrise-{}".format(zip)
    now = local_now()
    forecast = get_forecast(zip=zip)

    if not forecast.get("city") or not forecast["city"].get("sunrise"):
        log.error("Unable to get sunrise from forecast for zip: {}".format(zip))
        return None

    # Only trigger this once per day
    if same_day(_LAST_TRIGGERED_DATE.get(key), now):
        log.debug(
            "sunrise() already fired today @ {}".format(_LAST_TRIGGERED_DATE[key])
        )
        return None

    sunrisedt = datetime.fromtimestamp(
        forecast["city"]["sunrise"] + forecast["city"].get("timezone", 0), tz=tzlocal()
    )

    log.debug("Expected sunrise at {}".format(sunrisedt))

    log.debug("{} <= {} == {}".format(sunrisedt, now, sunrisedt <= now))

    if sunrisedt <= now:
        _LAST_TRIGGERED_DATE[key] = now
        return sunrisedt

    return None


def sunset(zip):
    """ When the sun is down """
    global _LAST_TRIGGERED_DATE

    key = "sunset-{}".format(zip)
    now = local_now()
    forecast = get_forecast(zip=zip)

    if not forecast.get("city") or not forecast["city"].get("sunset"):
        log.error("Unable to get sunset from forecast for zip: {}".format(zip))
        return None

    # Only trigger this once per day
    if same_day(_LAST_TRIGGERED_DATE.get(key), now):
        log.debug("sunset() already fired today @ {}".format(_LAST_TRIGGERED_DATE[key]))
        return None

    sunrisedt = datetime.fromtimestamp(
        forecast["city"]["sunrise"] + forecast["city"].get("timezone", 0), tz=tzlocal()
    )
    sunsetdt = datetime.fromtimestamp(
        forecast["city"]["sunset"] + forecast["city"].get("timezone", 0), tz=tzlocal()
    )

    log.debug("Expected sunrise at {}".format(sunrisedt))
    log.debug("Expected sunset at {}".format(sunsetdt))

    if sunsetdt <= now:
        _LAST_TRIGGERED_DATE[key] = now
        return sunsetdt

    return None


def precipitating(zip):
    """ If it is currently precipitating """
    raise NotImplementedError("precipitating not implemented")


CATALOG = {
    "sunrise": {"name": "Sunrise", "description": sunrise.__doc__, "func": sunrise,},
    "sunset": {"name": "Sunset", "description": sunset.__doc__, "func": sunset,},
    "precipitating": {
        "name": "Precipitating",
        "description": precipitating.__doc__,
        "func": precipitating,
    },
}
