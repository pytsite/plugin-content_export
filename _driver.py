"""PytSite Content Export Plugin Abstract Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from frozendict import frozendict
from plugins import widget


class Abstract(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        pass

    @abstractmethod
    def get_options_description(self, driver_options: frozendict) -> str:
        """Get human readable driver options
        """
        pass

    @abstractmethod
    def get_settings_widget(self, driver_options: frozendict, form_url: str) -> widget.Abstract:
        """Add widgets to the settings form of the driver
        """
        pass

    @abstractmethod
    def export(self, entity, exporter):
        """ Performs export.

        :type entity: plugins.content.model.Content
        :type exporter: plugins.content_export.model.ContentExport
        """
        pass
