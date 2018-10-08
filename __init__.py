"""PytSite Content Export Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _model as model, _error as error
from ._driver import Abstract as AbstractDriver
from ._api import register_driver


def plugin_load():
    from plugins import permissions, odm
    from . import _model

    # Permission group
    permissions.define_group('content_export', 'content_export@content_export')

    # ODM models
    odm.register_model('content_export', _model.ContentExport)


def plugin_load_wsgi():
    from pytsite import router, cron
    from plugins import admin
    from . import _eh

    # Admin sidebar menu
    m = 'content_export'
    admin.sidebar.add_menu(
        sid='content',
        mid=m,
        title=__name__ + '@export',
        path=router.rule_path('odm_ui@admin_browse', {'model': m}),
        icon='fa fa-bullhorn',
        permissions=(
            'odm_auth@create.content_export',
            'odm_auth@modify.content_export', 'odm_auth@modify_own.content_export',
            'odm_auth@delete.content_export', 'odm_auth@delete_own.content_export',
        ),
        weight=100
    )

    # Event handlers
    cron.every_min(_eh.cron_1min)
