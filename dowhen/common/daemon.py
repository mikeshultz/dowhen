import time
from datetime import datetime
from dowhen.trigger import get_triggers
from dowhen.do import Scheduler, load_do
from dowhen.when import load_when
from dowhen.config import config
from dowhen.common import getint
from dowhen.common.logger import get_logger

log = get_logger(__name__)

DEFAULT_TICK = 30


def when(name, kwargs):
    op = load_when(name)
    func = op['func']

    log.debug('Calling {} with kwargs: {}'.format(name, kwargs))

    return func(**kwargs)


def do(name, kwargs):
    op = load_do(name)
    func = op['func']

    log.debug('Calling {} with kwargs: {}'.format(name, kwargs))

    return func(**kwargs)


def run_daemon():
    log.debug('run_daemon()')

    scheduler = Scheduler()

    with config() as conf:
        log.debug('config()')
        while True:
            log.debug('--tick')

            try:
                triggers = get_triggers()

                for trig in triggers:
                    trigger_when = when(
                        trig['when']['name'],
                        trig['when'].get('args')
                    )

                    scheduler.add(trigger_when, trig['do']['name'], trig['do'].get('args'))

                schedule = scheduler.finalize()

                for event in schedule:
                    if not event.get('do'):
                        log.warn('Event {} has no action to perform'.format(
                            event[1]
                        ))
                        continue

                    do(event[1], event[2])

            except Exception:
                log.exception("Unhandled exception in daemon")

            time.sleep(getint(conf, 'tick', DEFAULT_TICK))
