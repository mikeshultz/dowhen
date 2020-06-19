import os
from pathlib import Path
from contextlib import contextmanager
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONF_DIR = os.environ.get("CONF_DIR", "~/.config/dowhen")
CONFIG_FILENAME = os.environ.get("CONFIG_FILENAME", "dowhen.yaml")
CACHED_CONFIG = None


def conf_dir():
    cd = Path(CONF_DIR).expanduser().resolve()

    if cd.exists() and cd.is_file():
        raise Exception("File exists where config directory should be!")

    if not cd.is_dir():
        cd.mkdir(mode=0o700, parents=True)

    return cd


def init_config():
    """ initialize and load configuration

    Usage
    -----
    _conf = init_config()
    myconfigvar = _conf.get("myconfigvar")
    """
    global CACHED_CONFIG

    confd = conf_dir()
    conf_file = confd.joinpath(CONFIG_FILENAME)

    # Create new config if one does not exist
    if not conf_file.is_file():
        with conf_file.open("x") as f:
            CACHED_CONFIG = {"triggers": []}
            dump(CACHED_CONFIG, f, Dumper=Dumper)

    # Load existing config
    else:
        with conf_file.open("r") as f:
            CACHED_CONFIG = load(f, Loader=Loader)

    return CACHED_CONFIG


@contextmanager
def config():
    conf = init_config()
    yield conf
    # TODO: Save?
