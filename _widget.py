"""PytSite Content Export Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang
from plugins import widget
from ._api import get_drivers


class DriverSelect(widget.select.Select):
    """Content Export Driver Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._items = sorted([(k, lang.t(v.get_description())) for k, v in get_drivers().items()])
