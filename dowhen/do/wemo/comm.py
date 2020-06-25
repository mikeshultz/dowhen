import pywemo
from datetime import datetime, timedelta

from dowhen.common import normalize_mac_address, local_now
from dowhen.common.logger import get_logger

log = get_logger(__name__)


CACHE_DURATION = timedelta(seconds=900)

_device_cache = []
_device_time = None


class DeviceNotFound(Exception):
    pass


def discover_wemo():
    """ Discover Wemo devices on the network """
    global _device_time, _device_cache

    if _device_time and _device_time - local_now() <= CACHE_DURATION:
        return _device_cache

    _device_cache = pywemo.discover_devices()
    _device_time = local_now()

    return _device_cache


def get_device(mac, devices=None):
    """ Get a specific device """
    global _device_time

    if not mac:
        return None
    if not devices:
        devices = discover_wemo()

    normal_mac = normalize_mac_address(mac)

    for dev in devices:
        if not dev or dev.mac is None:
            # Invalidate cache because this is bad
            _device_time = None
            log.warn(
                "Discovered device is missing its MAC address. Invalidating cache."
            )

        elif normalize_mac_address(dev.mac) == normal_mac:
            return dev

    return None


def device_on(mac):
    dev = get_device(mac)

    if not dev:
        raise DeviceNotFound("Device {} not found".format(mac))

    return dev.on()


def device_off(mac):
    dev = get_device(mac)

    if not dev:
        raise DeviceNotFound("Device {} not found".format(mac))

    return dev.off()


def device_toggle(mac):
    dev = get_device(mac)

    if not dev:
        raise DeviceNotFound("Device {} not found".format(mac))

    return dev.toggle()
