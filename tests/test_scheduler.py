from datetime import datetime, timedelta
from dowhen.do.util import Scheduler

DEVICE_ON = 'wemo.on'
DEVICE_OFF = 'wemo.off'


def test_scheduler():
    """ Test the Scheduler """

    s = Scheduler()

    one_time = datetime.now() + timedelta(minutes=15)
    two_time = datetime.now() + timedelta(minutes=20)
    three_time = datetime.now() + timedelta(minutes=25)

    # These stack, and the final on should prevail
    s.add(one_time, DEVICE_ON)
    s.add(two_time, DEVICE_OFF)
    s.add(three_time, DEVICE_ON)

    schedule = s.finalize()

    assert len(schedule) == 1
    assert schedule[0][0] == three_time
    assert schedule[0][1] == DEVICE_ON
