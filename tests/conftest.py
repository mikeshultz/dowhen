import os
from dowhen.common.logger import set_level

set_level(os.environ.get("LOG_LEVEL", "WARNING"))
