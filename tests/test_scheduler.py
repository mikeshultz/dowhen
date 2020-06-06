from datetime import datetime, timedelta
from dowhen.do.util import Scheduler

DEVICE_ON = 'wemo.on'
DEVICE_OFF = 'wemo.off'

DEVICE_ONE = '30:23:03:02:5D:1C'
DEVICE_TWO = '30:23:03:01:4E:68'


def test_scheduler():
    """ Test the Scheduler """

    s = Scheduler()

    one_time = datetime.now() + timedelta(minutes=15)
    two_time = datetime.now() + timedelta(minutes=20)
    three_time = datetime.now() + timedelta(minutes=25)

    # These stack, and the final on should prevail
    s.add(one_time, DEVICE_ON, {'mac': DEVICE_ONE})
    s.add(two_time, DEVICE_OFF, {'mac': DEVICE_ONE})
    s.add(three_time, DEVICE_ON, {'mac': DEVICE_ONE})

    schedule = s.finalize()

    assert len(schedule) == 1
    assert schedule[0][0] == three_time
    assert schedule[0][1] == DEVICE_ON
