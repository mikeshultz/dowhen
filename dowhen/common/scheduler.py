from dowhen.common import any_in_any
from dowhen.common.logger import get_logger
from dowhen.do.util import load_catalog

log = get_logger(__name__)


def create_call_key(name, args):
    """ Create a unique identifier for a call from the func name and args of the
    call """
    arg_hash = None
    if args:
        arg_hash = hash(frozenset(args.items()))
    key = "{}-{}".format(name, arg_hash)
    return key


class Event:
    """ An event to be scheduled """

    def __init__(self, when, name, args, attempt=0):
        self.when = when
        self.name = name
        self.args = args
        self.attempt = attempt


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
        mod, _ = name.split(".")

        if mod in self.catalogs:
            return self.catalogs[mod]

        self.catalogs[mod] = load_catalog(name)

        return self.catalogs[mod]

    def _get_stacks(self, name):
        _, funcname = name.split(".")
        cat = self._get_catalog(name)

        if funcname not in cat:
            return []

        return cat[funcname].get("stacks")

    def add(self, when, name, args=None):
        self.schedule.append(Event(when, name, args))

    def sort(self):
        self.schedule = list(sorted(self.schedule, key=lambda x: x.when, reverse=True))

    def squash(self):
        self.sort()

        seen = []
        new_schedule = []

        for item in self.schedule:
            mod, _ = item.name.split(".")
            call_key = create_call_key(item.name, item.args)

            if call_key in seen:
                continue

            # Get the other functions in the module that "stack" with this one
            stacks = self._get_stacks(item.name)

            # If this is stackable with a previously seen item, skip it
            if stacks and any_in_any(
                [create_call_key("{}.{}".format(mod, x), item.args) for x in stacks], seen
            ):
                continue

            seen.append(call_key)
            new_schedule.append(item)

        self.schedule = new_schedule

        return self.schedule

    def finalize(self):
        self.squash()

        schedule = self.schedule

        log.debug("Finalized Schedule")
        log.debug("------------------")
        for item in schedule:
            log.debug("{} - {}({})".format(item.when, item.name, item.args))

        self.schedule = []

        return schedule