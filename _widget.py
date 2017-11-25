"""PytSite Content Export Plugin Widgets
"""
from pytsite import lang as _lang
from plugins import widget as _widget
from ._api import get_drivers as _get_drivers

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class DriverSelect(_widget.select.Select):
    """Content Export Driver Select Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._items = sorted([(k, _lang.t(v.get_description())) for k, v in _get_drivers().items()])
