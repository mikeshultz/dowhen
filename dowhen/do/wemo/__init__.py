from dowhen.do.wemo.comm import device_on, device_off, device_toggle
from dowhen.common.logger import get_logger

log = get_logger(__name__)


def on(mac):
    """ Turn a Wemo device on """
    if mac is None:
        log.error("MAC address is None!")
        return

    log.info("Turning on WeMo device {}".format(mac))

    return device_on(mac)


def off(mac):
    """ Turn a Wemo device off """
    if mac is None:
        log.error("MAC address is None!")
        return

    log.info("Turning off WeMo device {}".format(mac))

    return device_off(mac)


def toggle(mac):
    """ Toggle a Wemo device """
    if mac is None:
        log.error("MAC address is None!")
        return

    log.info("Toggling WeMo device {}".format(mac))

    return device_toggle(mac)


CATALOG = {
    "on": {
        "name": "On",
        "description": on.__doc__,
        "func": on,
        "stacks": ["off", "toggle"],
    },
    "off": {
        "name": "Off",
        "description": off.__doc__,
        "func": off,
        "stacks": ["on", "toggle"],
    },
    "toggle": {
        "name": "Toggle",
        "description": toggle.__doc__,
        "func": toggle,
        "stacks": ["on", "off"],
    },
}
