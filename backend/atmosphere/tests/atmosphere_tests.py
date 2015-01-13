from nose.tools import *
from atmosphere.atmosphere import *


def test_store_exists():
    atmo = Atmosphere()
    assert hasattr(atmo, 'store')
