import json
from datetime import tzinfo, datetime
from unittest.mock import patch
from freezegun import freeze_time

from dowhen.when.openweathermap import sunrise
from dowhen.when.openweathermap.config import OWM_DATE_FORMAT

from .const import ZIP_1, ONE_AM, FIVE_AM, ONE_HOUR

TEST_JASON_FORECAST = """{"cod": "200", "message": 0, "cnt": 40, "list": [{"dt": 1592168400, "main": {"temp": 56.7, "feels_like": 49.05, "temp_min": 56.57, "temp_max": 56.7, "pressure": 1011, "sea_level": 1010, "grnd_level": 901, "humidity": 48, "temp_kf": 0.07}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 84}, "wind": {"speed": 8.72, "deg": 268}, "rain": {"3h": 1.65}, "sys": {"pod": "d"}, "dt_txt": "2020-06-14 21:00:00"}, {"dt": 1592179200, "main": {"temp": 55.96, "feels_like": 45.82, "temp_min": 55.72, "temp_max": 55.96, "pressure": 1011, "sea_level": 1011, "grnd_level": 902, "humidity": 42, "temp_kf": 0.13}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 92}, "wind": {"speed": 11.97, "deg": 261}, "rain": {"3h": 0.5}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 00:00:00"}, {"dt": 1592190000, "main": {"temp": 47.57, "feels_like": 41.74, "temp_min": 46.94, "temp_max": 47.57, "pressure": 1013, "sea_level": 1013, "grnd_level": 902, "humidity": 59, "temp_kf": 0.35}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 96}, "wind": {"speed": 4.54, "deg": 246}, "rain": {"3h": 0.34}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 03:00:00"}, {"dt": 1592200800, "main": {"temp": 41.22, "feels_like": 35.49, "temp_min": 41.09, "temp_max": 41.22, "pressure": 1015, "sea_level": 1015, "grnd_level": 902, "humidity": 72, "temp_kf": 0.07}, "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}], "clouds": {"all": 73}, "wind": {"speed": 4.05, "deg": 189}, "sys": {"pod": "n"}, "dt_txt": "2020-06-15 06:00:00"}, {"dt": 1592211600, "main": {"temp": 39.74, "feels_like": 34.3, "temp_min": 39.74, "temp_max": 39.74, "pressure": 1015, "sea_level": 1015, "grnd_level": 902, "humidity": 76, "temp_kf": 0}, "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03n"}], "clouds": {"all": 42}, "wind": {"speed": 3.51, "deg": 173}, "sys": {"pod": "n"}, "dt_txt": "2020-06-15 09:00:00"}, {"dt": 1592222400, "main": {"temp": 40.3, "feels_like": 34.72, "temp_min": 40.3, "temp_max": 40.3, "pressure": 1014, "sea_level": 1014, "grnd_level": 902, "humidity": 72, "temp_kf": 0}, "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}], "clouds": {"all": 59}, "wind": {"speed": 3.56, "deg": 164}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 12:00:00"}, {"dt": 1592233200, "main": {"temp": 52.34, "feels_like": 46.87, "temp_min": 52.34, "temp_max": 52.34, "pressure": 1011, "sea_level": 1011, "grnd_level": 901, "humidity": 48, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 100}, "wind": {"speed": 3.69, "deg": 184}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 15:00:00"}, {"dt": 1592244000, "main": {"temp": 60.42, "feels_like": 54.59, "temp_min": 60.42, "temp_max": 60.42, "pressure": 1010, "sea_level": 1010, "grnd_level": 902, "humidity": 41, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 100}, "wind": {"speed": 5.32, "deg": 234}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 18:00:00"}, {"dt": 1592254800, "main": {"temp": 59.86, "feels_like": 54.43, "temp_min": 59.86, "temp_max": 59.86, "pressure": 1010, "sea_level": 1010, "grnd_level": 902, "humidity": 49, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 100}, "wind": {"speed": 5.95, "deg": 306}, "sys": {"pod": "d"}, "dt_txt": "2020-06-15 21:00:00"}, {"dt": 1592265600, "main": {"temp": 51.53, "feels_like": 47.97, "temp_min": 51.53, "temp_max": 51.53, "pressure": 1010, "sea_level": 1010, "grnd_level": 900, "humidity": 79, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 100}, "wind": {"speed": 4.34, "deg": 316}, "rain": {"3h": 0.98}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 00:00:00"}, {"dt": 1592276400, "main": {"temp": 48.87, "feels_like": 46.8, "temp_min": 48.87, "temp_max": 48.87, "pressure": 1011, "sea_level": 1011, "grnd_level": 901, "humidity": 82, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 100}, "wind": {"speed": 1.05, "deg": 276}, "rain": {"3h": 0.86}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 03:00:00"}, {"dt": 1592287200, "main": {"temp": 46.47, "feels_like": 43.68, "temp_min": 46.47, "temp_max": 46.47, "pressure": 1011, "sea_level": 1011, "grnd_level": 900, "humidity": 82, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "clouds": {"all": 100}, "wind": {"speed": 1.45, "deg": 247}, "sys": {"pod": "n"}, "dt_txt": "2020-06-16 06:00:00"}, {"dt": 1592298000, "main": {"temp": 44.98, "feels_like": 41.76, "temp_min": 44.98, "temp_max": 44.98, "pressure": 1011, "sea_level": 1011, "grnd_level": 900, "humidity": 82, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "clouds": {"all": 100}, "wind": {"speed": 1.72, "deg": 227}, "sys": {"pod": "n"}, "dt_txt": "2020-06-16 09:00:00"}, {"dt": 1592308800, "main": {"temp": 45.91, "feels_like": 42.93, "temp_min": 45.91, "temp_max": 45.91, "pressure": 1012, "sea_level": 1012, "grnd_level": 901, "humidity": 84, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 100}, "wind": {"speed": 1.83, "deg": 267}, "rain": {"3h": 0.47}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 12:00:00"}, {"dt": 1592319600, "main": {"temp": 50.43, "feels_like": 47.71, "temp_min": 50.43, "temp_max": 50.43, "pressure": 1012, "sea_level": 1012, "grnd_level": 901, "humidity": 75, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 92}, "wind": {"speed": 1.9, "deg": 261}, "rain": {"3h": 0.49}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 15:00:00"}, {"dt": 1592330400, "main": {"temp": 56.01, "feels_like": 51.58, "temp_min": 56.01, "temp_max": 56.01, "pressure": 1011, "sea_level": 1011, "grnd_level": 902, "humidity": 61, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 89}, "wind": {"speed": 4.9, "deg": 282}, "rain": {"3h": 1.01}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 18:00:00"}, {"dt": 1592341200, "main": {"temp": 57.18, "feels_like": 51.96, "temp_min": 57.18, "temp_max": 57.18, "pressure": 1010, "sea_level": 1010, "grnd_level": 901, "humidity": 59, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 98}, "wind": {"speed": 6.42, "deg": 300}, "rain": {"3h": 1.73}, "sys": {"pod": "d"}, "dt_txt": "2020-06-16 21:00:00"}, {"dt": 1592352000, "main": {"temp": 55.13, "feels_like": 51.08, "temp_min": 55.13, "temp_max": 55.13, "pressure": 1009, "sea_level": 1009, "grnd_level": 900, "humidity": 65, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 99}, "wind": {"speed": 4.56, "deg": 317}, "rain": {"3h": 2.1}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 00:00:00"}, {"dt": 1592362800, "main": {"temp": 49.26, "feels_like": 45.84, "temp_min": 49.26, "temp_max": 49.26, "pressure": 1011, "sea_level": 1011, "grnd_level": 901, "humidity": 76, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 100}, "wind": {"speed": 2.86, "deg": 292}, "rain": {"3h": 1.15}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 03:00:00"}, {"dt": 1592373600, "main": {"temp": 42.69, "feels_like": 38.3, "temp_min": 42.69, "temp_max": 42.69, "pressure": 1014, "sea_level": 1014, "grnd_level": 902, "humidity": 81, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "clouds": {"all": 100}, "wind": {"speed": 2.98, "deg": 244}, "sys": {"pod": "n"}, "dt_txt": "2020-06-17 06:00:00"}, {"dt": 1592384400, "main": {"temp": 39.67, "feels_like": 35.04, "temp_min": 39.67, "temp_max": 39.67, "pressure": 1015, "sea_level": 1015, "grnd_level": 903, "humidity": 83, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "clouds": {"all": 100}, "wind": {"speed": 2.68, "deg": 251}, "sys": {"pod": "n"}, "dt_txt": "2020-06-17 09:00:00"}, {"dt": 1592395200, "main": {"temp": 42.1, "feels_like": 38.07, "temp_min": 42.1, "temp_max": 42.1, "pressure": 1017, "sea_level": 1017, "grnd_level": 905, "humidity": 82, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 100}, "wind": {"speed": 2.24, "deg": 203}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 12:00:00"}, {"dt": 1592406000, "main": {"temp": 46.96, "feels_like": 42.66, "temp_min": 46.96, "temp_max": 46.96, "pressure": 1017, "sea_level": 1017, "grnd_level": 906, "humidity": 77, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 100}, "wind": {"speed": 3.74, "deg": 228}, "rain": {"3h": 0.13}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 15:00:00"}, {"dt": 1592416800, "main": {"temp": 54.23, "feels_like": 49.96, "temp_min": 54.23, "temp_max": 54.23, "pressure": 1017, "sea_level": 1017, "grnd_level": 907, "humidity": 59, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 99}, "wind": {"speed": 3.69, "deg": 261}, "rain": {"3h": 0.42}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 18:00:00"}, {"dt": 1592427600, "main": {"temp": 59.58, "feels_like": 51.84, "temp_min": 59.58, "temp_max": 59.58, "pressure": 1016, "sea_level": 1016, "grnd_level": 907, "humidity": 45, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 95}, "wind": {"speed": 9.19, "deg": 274}, "rain": {"3h": 0.48}, "sys": {"pod": "d"}, "dt_txt": "2020-06-17 21:00:00"}, {"dt": 1592438400, "main": {"temp": 60.58, "feels_like": 53.13, "temp_min": 60.58, "temp_max": 60.58, "pressure": 1016, "sea_level": 1016, "grnd_level": 907, "humidity": 44, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 91}, "wind": {"speed": 8.81, "deg": 293}, "rain": {"3h": 0.2}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 00:00:00"}, {"dt": 1592449200, "main": {"temp": 52.07, "feels_like": 48.31, "temp_min": 52.07, "temp_max": 52.07, "pressure": 1017, "sea_level": 1017, "grnd_level": 907, "humidity": 64, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 94}, "wind": {"speed": 2.82, "deg": 296}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 03:00:00"}, {"dt": 1592460000, "main": {"temp": 45.43, "feels_like": 42.03, "temp_min": 45.43, "temp_max": 45.43, "pressure": 1019, "sea_level": 1019, "grnd_level": 907, "humidity": 77, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "clouds": {"all": 94}, "wind": {"speed": 1.66, "deg": 205}, "sys": {"pod": "n"}, "dt_txt": "2020-06-18 06:00:00"}, {"dt": 1592470800, "main": {"temp": 43.3, "feels_like": 39.61, "temp_min": 43.3, "temp_max": 43.3, "pressure": 1019, "sea_level": 1019, "grnd_level": 907, "humidity": 80, "temp_kf": 0}, "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}], "clouds": {"all": 78}, "wind": {"speed": 1.79, "deg": 178}, "sys": {"pod": "n"}, "dt_txt": "2020-06-18 09:00:00"}, {"dt": 1592481600, "main": {"temp": 43.21, "feels_like": 39.69, "temp_min": 43.21, "temp_max": 43.21, "pressure": 1019, "sea_level": 1019, "grnd_level": 907, "humidity": 80, "temp_kf": 0}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}], "clouds": {"all": 86}, "wind": {"speed": 1.48, "deg": 194}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 12:00:00"}, {"dt": 1592492400, "main": {"temp": 55.33, "feels_like": 52.7, "temp_min": 55.33, "temp_max": 55.33, "pressure": 1017, "sea_level": 1017, "grnd_level": 907, "humidity": 63, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 70}, "wind": {"speed": 1.79, "deg": 200}, "rain": {"3h": 0.35}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 15:00:00"}, {"dt": 1592503200, "main": {"temp": 63.43, "feels_like": 59.49, "temp_min": 63.43, "temp_max": 63.43, "pressure": 1016, "sea_level": 1016, "grnd_level": 908, "humidity": 45, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 82}, "wind": {"speed": 3.65, "deg": 235}, "rain": {"3h": 0.32}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 18:00:00"}, {"dt": 1592514000, "main": {"temp": 66.9, "feels_like": 63.1, "temp_min": 66.9, "temp_max": 66.9, "pressure": 1014, "sea_level": 1014, "grnd_level": 907, "humidity": 42, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 95}, "wind": {"speed": 3.89, "deg": 288}, "rain": {"3h": 0.59}, "sys": {"pod": "d"}, "dt_txt": "2020-06-18 21:00:00"}, {"dt": 1592524800, "main": {"temp": 65.79, "feels_like": 61.74, "temp_min": 65.79, "temp_max": 65.79, "pressure": 1015, "sea_level": 1015, "grnd_level": 907, "humidity": 41, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 82}, "wind": {"speed": 3.74, "deg": 314}, "rain": {"3h": 0.4}, "sys": {"pod": "d"}, "dt_txt": "2020-06-19 00:00:00"}, {"dt": 1592535600, "main": {"temp": 56.39, "feels_like": 53.55, "temp_min": 56.39, "temp_max": 56.39, "pressure": 1016, "sea_level": 1016, "grnd_level": 906, "humidity": 60, "temp_kf": 0}, "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}], "clouds": {"all": 44}, "wind": {"speed": 2.06, "deg": 340}, "sys": {"pod": "d"}, "dt_txt": "2020-06-19 03:00:00"}, {"dt": 1592546400, "main": {"temp": 48.58, "feels_like": 45.9, "temp_min": 48.58, "temp_max": 48.58, "pressure": 1018, "sea_level": 1018, "grnd_level": 906, "humidity": 74, "temp_kf": 0}, "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}], "clouds": {"all": 51}, "wind": {"speed": 1.05, "deg": 323}, "sys": {"pod": "n"}, "dt_txt": "2020-06-19 06:00:00"}, {"dt": 1592557200, "main": {"temp": 45.77, "feels_like": 43.3, "temp_min": 45.77, "temp_max": 45.77, "pressure": 1018, "sea_level": 1018, "grnd_level": 906, "humidity": 79, "temp_kf": 0}, "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}], "clouds": {"all": 63}, "wind": {"speed": 0.31, "deg": 160}, "sys": {"pod": "n"}, "dt_txt": "2020-06-19 09:00:00"}, {"dt": 1592568000, "main": {"temp": 44.13, "feels_like": 41.11, "temp_min": 44.13, "temp_max": 44.13, "pressure": 1019, "sea_level": 1019, "grnd_level": 907, "humidity": 80, "temp_kf": 0}, "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}], "clouds": {"all": 36}, "wind": {"speed": 0.87, "deg": 132}, "sys": {"pod": "d"}, "dt_txt": "2020-06-19 12:00:00"}, {"dt": 1592578800, "main": {"temp": 59.25, "feels_like": 57.13, "temp_min": 59.25, "temp_max": 59.25, "pressure": 1018, "sea_level": 1018, "grnd_level": 909, "humidity": 56, "temp_kf": 0}, "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}], "clouds": {"all": 34}, "wind": {"speed": 1.12, "deg": 178}, "sys": {"pod": "d"}, "dt_txt": "2020-06-19 15:00:00"}, {"dt": 1592589600, "main": {"temp": 73.02, "feels_like": 70.9, "temp_min": 73.02, "temp_max": 73.02, "pressure": 1016, "sea_level": 1016, "grnd_level": 909, "humidity": 37, "temp_kf": 0}, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}], "clouds": {"all": 18}, "wind": {"speed": 1.79, "deg": 247}, "rain": {"3h": 0.24}, "sys": {"pod": "d"}, "dt_txt": "2020-06-19 18:00:00"}], "city": {"name": "Missoula", "coord": {"lat": 46.8563, "lon": -114.0252}, "country": "US", "timezone": -21600, "sunrise": 1592134869, "sunset": 1592191919}}"""


def generate_sunrise(dt):
    obj = json.loads(TEST_JASON_FORECAST)
    obj['city']['sunrise'] = datetime.timestamp(
        dt
    )
    obj['city']['timezone'] = 0
    return obj


@patch('dowhen.when.openweathermap.get_forecast', autospec=True)
def test_owm_sunrise(mock_get_forecast):
    """ Test the Open Weather Map sunrise trigger """
    mock_get_forecast.return_value = generate_sunrise(FIVE_AM)

    with freeze_time(ONE_AM):
        tres = sunrise(ZIP_1)
        assert tres is None

    with freeze_time(FIVE_AM):
        tres = sunrise(ZIP_1)
        assert tres is not None
        assert tres == FIVE_AM

    # Should only trigger once
    with freeze_time(FIVE_AM + ONE_HOUR):
        tres = sunrise(ZIP_1)
        assert tres is None
