import time
from dowhen.trigger import get_triggers
from dowhen.do import load_do
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
    with config() as conf:
        log.debug('config()')
        while True:
            log.debug('--tick')

            try:
                triggers = get_triggers()

                for trig in triggers:
                    triggered = when(
                        trig['when']['name'],
                        trig['when'].get('args')
                    )

                    if triggered:
                        log.info('{} triggered!'.format(trig['when']['name']))

                        if trig['do']:
                            for work in trig['do']:
                                do(work['name'], work['args'])

            except Exception:
                log.exception("Unhandled exception in daemon")

            time.sleep(getint(conf, 'tick', DEFAULT_TICK))
