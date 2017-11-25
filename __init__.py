"""PytSite Content Export Plugin
"""
# Public API
from . import _model as model, _error as error
from ._driver import Abstract as AbstractDriver
from ._api import register_driver

# Locally necessary imports
from pytsite import events as _events, lang as _lang, router as _router
from plugins import permissions as _permissions, odm as _odm, admin as _admin
from . import _model, _eh

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Resources
_lang.register_package(__name__)

# Permission group
_permissions.define_group('content_export', 'content_export@content_export')

# ODM models
_odm.register_model('content_export', _model.ContentExport)

# Event handlers
_events.listen('pytsite.cron.1min', _eh.cron_1min)

# Admin sidebar menu
m = 'content_export'
_admin.sidebar.add_menu(sid='content', mid=m, title=__name__ + '@export',
                        href=_router.rule_path('odm_ui@browse', {'model': m}),
                        icon='fa fa-bullhorn',
                        permissions=('odm_auth.view.' + m, 'odm_auth.view_own.' + m),
                        weight=100)
