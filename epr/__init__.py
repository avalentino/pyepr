import atexit
import _epr
_epr._init_api()
atexit.register(_epr._close_api)
del atexit

from _epr import *
