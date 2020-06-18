import requests
from datetime import datetime
from dateutil.tz import tzlocal
from dowhen.common import local_now
from dowhen.common.logger import get_logger

from dowhen.when.openweathermap.config import (
    OWM_API_KEY,
    FORECAST_API,
    OWM_DATE_FORMAT,
    DEFAULT_ZIP,
    DEFAULT_COUNTRY_CODE,
)

log = get_logger(__name__)

FORECAST_CACHE = None
FORECAST_CACHE_TIME = None


def parse_owm_date(v):
    return datetime.strptime(v, OWM_DATE_FORMAT).replace(tzinfo=tzlocal())


def fetch_forecast_data(zip, country_code):
    url = FORECAST_API.format(api_key=OWM_API_KEY, country_code=country_code, zip=zip,)
    r = requests.get(url)
    assert r.status_code == 200, "Bad response from OWM"
    return r.json()


def get_forecast(zip=DEFAULT_ZIP, country_code=DEFAULT_COUNTRY_CODE):
    """ Get the 5 day forecast for a zip """
    global FORECAST_CACHE, FORECAST_CACHE_TIME

    if FORECAST_CACHE is not None and FORECAST_CACHE_TIME > local_now():
        return FORECAST_CACHE

    FORECAST_CACHE = fetch_forecast_data(zip, country_code)
    forecast_list = FORECAST_CACHE.get("list")
    if forecast_list is not None and len(forecast_list) > 0:
        date_string = forecast_list[0].get("dt_txt")
        if date_string is not None:
            FORECAST_CACHE_TIME = parse_owm_date(date_string)
            log.debug("Set Forecast cache time to {}".format(FORECAST_CACHE_TIME))
        else:
            log.warn("dt_txt has invalid value or does not exist")

    return FORECAST_CACHE
