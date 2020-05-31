from dowhen.do.wemo.comm import device_on, device_off, device_toggle
from dowhen.common.logger import get_logger

log = get_logger(__name__)


def on(mac):
    """ Turn a Wemo device on """
    log.info('Turning on WeMo device {}'.format(mac))
    return device_on(mac)


def off(mac):
    """ Turn a Wemo device off """
    log.info('Turning off WeMo device {}'.format(mac))
    return device_off(mac)


def toggle(mac):
    """ Toggle a Wemo device """
    log.info('Toggling WeMo device {}'.format(mac))
    return device_toggle(mac)


CATALOG = {
    'on': {
        'name': 'On',
        'description': on.__doc__,
        'func': on,
    },
    'off': {
        'name': 'Off',
        'description': off.__doc__,
        'func': off,
    },
    'toggle': {
        'name': 'Toggle',
        'description': toggle.__doc__,
        'func': toggle,
    },
}
