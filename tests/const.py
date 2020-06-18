import datetime
from dateutil.tz import tzlocal

YEAR = 2020
MONTH = 6
DAY = 11

# Times
ONE_AM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=1, minute=0, second=0, tzinfo=tzlocal()
)
ONE_PM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=13, minute=0, second=0, tzinfo=tzlocal()
)
TWELVE_FIFTY_NINE_AM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=0, minute=59, second=0, tzinfo=tzlocal()
)
TWELVE_FIFTY_NINE_PM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=12, minute=59, second=0, tzinfo=tzlocal()
)
FIVE_AM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=5, minute=0, second=0, tzinfo=tzlocal()
)
FIVE_PM = datetime.datetime(
    year=YEAR, month=MONTH, day=DAY, hour=17, minute=0, second=0, tzinfo=tzlocal()
)

# Intervals
ONE_DAY = datetime.timedelta(hours=24)
ONE_HOUR = datetime.timedelta(hours=1)
ONE_MINUTE = datetime.timedelta(minutes=1)
TEN_SECONDS = datetime.timedelta(seconds=10)

# Locations
ZIP_1 = 59801
COUNTRY_CODE_1 = "us"
CITY_1 = "Missoula"
