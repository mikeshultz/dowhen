from importlib import import_module
from dowhen.common.logger import get_logger

log = get_logger(__name__)

ENABLED_MODULES = ['wemo']


def load_do(name):
    """ Loads a "do" func """
    path = name.split('.')

    if len(path) != 2:
        raise Exception('{} does not appear to be a valid "do" func'.format(
            name
        ))

    if path[0] not in ENABLED_MODULES:
        raise Exception('Module does not exist')

    mod_path = 'dowhen.do.{}'.format(path[0])

    log.debug('Importing {}'.format(mod_path))

    mod = import_module(mod_path)

    if not mod.CATALOG.get(path[1]):
        raise Exception('{} was not found in module catalog'.format(name))

    return mod.CATALOG.get(path[1])
