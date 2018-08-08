"""PytSite Content Export Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class DriverRegistered(Exception):
    pass


class DriverNotRegistered(Exception):
    pass


class ExportError(Exception):
    pass
