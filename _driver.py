"""PytSite Content Export Plugin Abstract Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from frozendict import frozendict as _frozendict
from plugins import widget as _widget


class Abstract(_ABC):
    @_abstractmethod
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        pass

    @_abstractmethod
    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        pass

    @_abstractmethod
    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options
        """
        pass

    @_abstractmethod
    def get_settings_widget(self, driver_options: _frozendict, form_url: str) -> _widget.Abstract:
        """Add widgets to the settings form of the driver
        """
        pass

    @_abstractmethod
    def export(self, entity, exporter):
        """ Performs export.

        :type entity: plugins.content.model.Content
        :type exporter: plugins.content_export.model.ContentExport
        """
        pass
