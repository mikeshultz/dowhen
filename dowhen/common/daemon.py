import time
from datetime import datetime
from dowhen.trigger import get_triggers
from dowhen.do import load_do
from dowhen.when import load_when
from dowhen.config import config
from dowhen.common import getint, local_now
from dowhen.common.scheduler import MaxRetriesReached, Scheduler
from dowhen.common.logger import get_logger

log = get_logger(__name__)

DEFAULT_TICK = 30


def when(name, kwargs):
    op = load_when(name)
    func = op["func"]

    log.debug("Calling {} with kwargs: {}".format(name, kwargs))

    return func(**kwargs)


def do(name, kwargs):
    op = load_do(name)
    func = op["func"]

    log.debug("Calling {} with kwargs: {}".format(name, kwargs))

    return func(**kwargs)


def run_daemon():
    log.debug("run_daemon()")

    scheduler = Scheduler()

    with config() as conf:
        log.debug("config()")
        while True:
            log.debug("--tick {}".format(local_now()))

            try:
                triggers = get_triggers()

                for trig in triggers:
                    trigger_when = when(trig["when"]["name"], trig["when"].get("args"))

                    if trigger_when:
                        for action in trig["do"]:
                            scheduler.add(
                                trigger_when, action["name"], action.get("args")
                            )

                log.debug("Scheduler has {} actions".format(len(scheduler.schedule)))

                executing = True
                while executing:

                    schedule = scheduler.finalize()

                    log.info("Will perform {} actions".format(len(schedule)))

                    for event in schedule:
                        try:
                            do(event.name, event.args)
                        except MaxRetriesReached:
                            log.exception(
                                "Maximum retries reached for {}({}".format(
                                    event.name, event.cargs
                                )
                            )
                        except Exception:
                            log.exception(
                                "Exception while attempting to perform action {}({}). Retrying...".format(
                                    event.name, event.args
                                )
                            )
                            scheduler.retry(event)

                    if len(scheduler.schedule) < 1:
                        executing = False

            except Exception:
                log.exception("Unhandled exception in daemon")

            time.sleep(getint(conf, "tick", DEFAULT_TICK))
