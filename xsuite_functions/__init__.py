on__ = "v0.0.1"

from .functions import *

from pathlib import Path
_pkg_root = Path(__file__).parent.absolute()
del(Path)
