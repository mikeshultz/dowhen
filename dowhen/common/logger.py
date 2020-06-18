import logging

_LOGGER = None
_CONSOLE_HANDLER = None


def get_root():
    global _LOGGER, _CONSOLE_HANDLER

    if _LOGGER is None:
        _LOGGER = logging.getLogger("dowhen")
        _CONSOLE_HANDLER = logging.StreamHandler()

        fmt = logging.Formatter("%(levelname)8s %(message)s")
        _CONSOLE_HANDLER.setFormatter(fmt)

        _CONSOLE_HANDLER.setLevel(logging.INFO)
        _LOGGER.setLevel(logging.INFO)

        _LOGGER.addHandler(_CONSOLE_HANDLER)

    return _LOGGER


def set_level(log_level):
    global _CONSOLE_HANDLER

    root = get_root()
    _LOGGER.setLevel(log_level)
    _CONSOLE_HANDLER.setLevel(log_level)
    root.debug("Set log level to: {}".format(log_level))


def get_logger(name):
    root = get_root()
    return root.getChild(name)
