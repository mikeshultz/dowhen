"""
When Module Spec

All modules should take advantage of python's self doc features.  All usable
"when" functions should be available for import in from module's __init__.py and
be enumerable from a `CATALOG` var available from __init__.py.  An example:

    CATALOG = {
        'sunrise': {
            'name': 'Sunrise',
            'description': sunrise.__doc__,
            'func': sunrise,
        }
    }

Every when check is a function that will return boolean according to whether or
not the "when" condition has been met.

For example, if we want to detect sunrise, `sunrise()` should return Frue if the
sun is risen according to the data source.  It would then return False once the
sun has set.  The inverse functionality would happen with `sunset()`.

These functions will be continuously called to check against the "do schedule."
The modules may cache as they see fit.
"""
from importlib import import_module
from dowhen.common.logger import get_logger

log = get_logger(__name__)

ENABLED_MODULES = ["datetime", "openweathermap"]


def load_when(name):
    """ Loads a "when" func """
    path = name.split(".")

    if len(path) != 2:
        raise Exception('{} does not appear to be a valid "when" func'.format(name))

    if path[0] not in ENABLED_MODULES:
        raise Exception("Module does not exist")

    mod_path = "dowhen.when.{}".format(path[0])

    log.debug("Importing {}".format(mod_path))

    mod = import_module(mod_path)

    if not mod.CATALOG.get(path[1]):
        raise Exception("{} was not found in module catalog".format(name))

    return mod.CATALOG.get(path[1])
