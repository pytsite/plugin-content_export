"""PytSite Content Export Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict
from . import _driver, _error

_drivers = {}


def register_driver(driver: _driver.Abstract):
    """Register export driver.
    """
    name = driver.get_name()

    if name in _drivers:
        raise _error.DriverRegistered("Driver with name '{}' is already registered.".format(name))

    _drivers[name] = driver


def get_driver(name: str) -> _driver.Abstract:
    """Get driver instance.
    """
    if name not in _drivers:
        raise _error.DriverNotRegistered("Driver with name '{}' is not registered.".format(name))

    return _drivers[name]


def get_drivers() -> frozendict:
    """Get registered drivers.
    """
    return frozendict(_drivers)
