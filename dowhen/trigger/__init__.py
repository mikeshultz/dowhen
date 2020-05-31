"""
Every trigger consists of:
- when
- once/every
- do

users?
enable/disable?

triggers:
  - openweathermap.sunrise:
    - wemo.on: 30:23:03:01:4E:68
    - wemo.on: 30:23:03:01:16:46
"""
from dowhen.config import config


def get_triggers():
    with config() as conf:
        return conf.get('triggers')
