import os
from dowhen.config import init_config

_conf = init_config()

OWM_API_KEY = os.environ.get("OWM_API_KEY", _conf.get("owm_api_key"))
OWM_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORECAST_API = "https://api.openweathermap.org/data/2.5/forecast?zip={zip},{country_code}&appid={api_key}&units=imperial"
DEFAULT_ZIP = 90210
DEFAULT_COUNTRY_CODE = "US"
