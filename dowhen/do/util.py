from importlib import import_module

from dowhen.common import any_in_any
from dowhen.common.logger import get_logger

log = get_logger(__name__)

ENABLED_MODULES = ['wemo']

_schedule = []


def load_module(name):
    path = name.split('.')

    if len(path) != 2:
        raise Exception('{} does not appear to be a valid "do" func'.format(
            name
        ))

    if path[0] not in ENABLED_MODULES:
        raise Exception('Module does not exist')

    mod_path = 'dowhen.do.{}'.format(path[0])

    log.debug('Importing {}'.format(mod_path))

    return import_module(mod_path)


def load_catalog(name):
    mod = load_module(name)
    return mod.CATALOG


def load_do(name):
    """ Loads a "do" func """

    path = name.split('.')
    catalog = load_catalog(name)

    if not catalog.get(path[1]):
        raise Exception('{} was not found in module catalog'.format(name))

    return catalog[path[1]]


def create_call_key(name, args):
    """ Create a unique identifier for a call from the func name and args of the
    call """
    arg_hash = None
    if args:
        arg_hash = hash(frozenset(args.items()))
    key = '{}-{}'.format(name, arg_hash)
    return key


class Scheduler:
    """ This scheduler accepts timed "do" events that came from "when" triggers.
    Its purpose is to remove duplicates and collapse stackable "do" actions.
    This will prevent too many events firing when initially starting the
    service. For instance, it will prevent things like flickering lights.
    """

    def __init__(self):
        self.schedule = []
        self.catalogs = {}

    def _get_catalog(self, name):
        mod, _ = name.split('.')

        if mod in self.catalogs:
            return self.catalogs[mod]

        self.catalogs[mod] = load_catalog(name)

        return self.catalogs[mod]

    def _get_stacks(self, name):
        _, funcname = name.split('.')
        cat = self._get_catalog(name)

        if funcname not in cat:
            return []

        return cat[funcname].get('stacks')

    def add(self, when, name, args=None):
        self.schedule.append((when, name, args))

    def sort(self):
        self.schedule = list(sorted(self.schedule, key=lambda x: x[0], reverse=True))

    def squash(self):
        self.sort()

        seen = []
        new_schedule = []

        for item in self.schedule:
            _, name, args = item
            mod, _ = name.split('.')
            call_key = create_call_key(name, args)

            if call_key in seen:
                continue

            # Get the other functions in the module that "stack" with this one
            stacks = self._get_stacks(name)

            # If this is stackable with a previously seen item, skip it
            if stacks and any_in_any(
                [create_call_key('{}.{}'.format(mod, x), args) for x in stacks],
                seen
            ):
                continue

            seen.append(call_key)
            new_schedule.append(item)

        self.schedule = new_schedule

        return self.schedule

    def finalize(self):
        self.squash()

        schedule = self.schedule

        log.debug('Finalized Schedule')
        log.debug('------------------')
        for item in schedule:
            log.debug('{} - {}({})'.format(item[0], item[1], item[2]))

        self.schedule = []

        return schedule
