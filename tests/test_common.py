from dowhen.common import (
    getint,
    normalize_mac_address,
    same_day,
    same_hour,
    same_minute,
    any_in_any,
)

from .const import ONE_AM, ONE_DAY, ONE_HOUR, ONE_MINUTE, TEN_SECONDS


def test_getint():
    """ Test the getint comparison function """
    test_dict = {
        'int': 1,
        'str': '1',
        'float': 1.0,
    }

    ret_int = getint(test_dict, 'int')
    assert ret_int is not None
    assert type(ret_int) == int

    ret_str = getint(test_dict, 'str')
    assert ret_str is not None
    assert type(ret_str) == int

    ret_float = getint(test_dict, 'float')
    assert ret_float is not None
    assert type(ret_float) == int

    ret_default = getint(test_dict, 'nothing')
    assert ret_default is None


def test_normalize_mac_address():
    """ Test the normalize_mac_address comparison function """
    test_mac_standard = '54:e1:ad:c6:af:52'
    test_mac_wemo1 = '54e1adc6af52'
    test_mac_wemo2 = '54E1ADC6AF52'

    assert normalize_mac_address(test_mac_standard) == normalize_mac_address(test_mac_wemo1)
    assert normalize_mac_address(test_mac_standard) == normalize_mac_address(test_mac_wemo2)


def test_same_day():
    """ Test the same_day comparison function """
    assert same_day(ONE_AM, ONE_AM + TEN_SECONDS) is True
    assert same_day(ONE_AM, ONE_AM + ONE_MINUTE) is True
    assert same_day(ONE_AM, ONE_AM + ONE_HOUR) is True
    assert same_day(ONE_AM, ONE_AM + ONE_DAY) is False


def test_same_hour():
    """ Test the same_hour comparison function """
    assert same_hour(ONE_AM, ONE_AM + TEN_SECONDS) is True
    assert same_hour(ONE_AM, ONE_AM + ONE_MINUTE) is True
    assert same_hour(ONE_AM, ONE_AM + ONE_HOUR) is False
    assert same_hour(ONE_AM, ONE_AM + ONE_DAY) is False


def test_same_minute():
    """ Test the same_minute comparison function """
    assert same_minute(ONE_AM, ONE_AM + TEN_SECONDS) is True
    assert same_minute(ONE_AM, ONE_AM + ONE_MINUTE) is False
    assert same_minute(ONE_AM, ONE_AM + ONE_HOUR) is False
    assert same_minute(ONE_AM, ONE_AM + ONE_DAY) is False


def test_any_in_any():
    """ Test the any_in_any comparison function """
    assert any_in_any([1, 2, 3, 9], [6, 7, 8, 9]) is True
    assert any_in_any([1, 2, 3, 4], [6, 7, 8, 9]) is False
