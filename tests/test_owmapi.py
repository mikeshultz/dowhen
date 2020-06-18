import pytest

from dowhen.when.openweathermap.owmapi import fetch_forecast_data, get_forecast

from .const import COUNTRY_CODE_1, CITY_1, ZIP_1


def assert_owmapi_results(results):
    print("results", results)
    assert type(results) == dict
    assert results.get("cod") == "200"

    assert results.get("city") is not None
    assert type(results.get("city")) == dict
    assert results["city"].get("name") == CITY_1
    assert results["city"].get("country") == COUNTRY_CODE_1.upper()

    assert results.get("list") is not None
    assert type(results["list"]) == list
    assert len(results["list"]) > 0

    for item in results["list"]:
        # TODO: Fill this out with what we use
        assert item.get("dt") is not None
        assert item.get("dt_txt") is not None
        assert item.get("main") is not None
        assert type(item["main"]) == dict
        assert item["main"].get("temp_min") is not None
        assert item["main"].get("temp_max") is not None


@pytest.mark.skip(reason="Can't test without an API key")
def test_owmapi_fetch():
    """ Test the Open Weather Map API forecast fetch """
    assert_owmapi_results(fetch_forecast_data(ZIP_1, COUNTRY_CODE_1))


@pytest.mark.skip(reason="Can't test without an API key")
def test_owmapi_forecast():
    """ Test the Open Weather Map API forecast call """
    result1 = get_forecast(ZIP_1, COUNTRY_CODE_1)
    assert_owmapi_results(result1)

    # Test cache
    result2 = get_forecast(ZIP_1, COUNTRY_CODE_1)
    assert_owmapi_results(result2)

    assert result1["list"][0]["dt"] == result2["list"][0]["dt"]
