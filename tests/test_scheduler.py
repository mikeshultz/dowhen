from datetime import datetime, timedelta
from dowhen.common import local_now
from dowhen.common.scheduler import MaxRetriesReached, Scheduler

DEVICE_ON = "wemo.on"
DEVICE_OFF = "wemo.off"

DEVICE_ONE = "30:23:03:02:5D:1C"
DEVICE_TWO = "30:23:03:01:4E:68"


def test_scheduler():
    """ Test the Scheduler """

    s = Scheduler()

    one_time = local_now() + timedelta(minutes=15)
    two_time = local_now() + timedelta(minutes=20)
    three_time = local_now() + timedelta(minutes=25)

    # These stack, and the final on should prevail
    s.add(one_time, DEVICE_ON, {"mac": DEVICE_ONE})
    s.add(two_time, DEVICE_OFF, {"mac": DEVICE_ONE})
    s.add(three_time, DEVICE_ON, {"mac": DEVICE_ONE})

    schedule = s.finalize()

    assert len(schedule) == 1
    assert schedule[0].when == three_time
    assert schedule[0].name == DEVICE_ON
    assert type(schedule[0].args) == dict
    assert schedule[0].args.get("mac") == DEVICE_ONE


def test_scheduler_max_retries():
    """ Test max retries on scheduler """

    s = Scheduler()

    when = local_now() + timedelta(minutes=15)

    s.add(when, "test.echo", {"string": "Hello, world!"})

    assert len(s.schedule) == 1

    first_schedule = s.finalize()

    assert len(first_schedule) == 1
    assert first_schedule[0].retries == 0

    s.retry(first_schedule[0])

    first_schedule = s.finalize()

    assert len(first_schedule) == 1
    assert first_schedule[0].retries == 1

    s.retry(first_schedule[0])

    first_schedule = s.finalize()

    assert len(first_schedule) == 1
    assert first_schedule[0].retries == 2

    s.retry(first_schedule[0])

    first_schedule = s.finalize()

    assert len(first_schedule) == 1
    assert first_schedule[0].retries == 3

    try:
        s.retry(first_schedule[0])
        assert False, "Should have raised an exception"
    except MaxRetriesReached:
        pass
    except AssertionError as err:
        raise err
    except Exception as err:
        assert False, "Wrong exception seen: {}".format(err)
