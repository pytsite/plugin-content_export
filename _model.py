"""PytSite Content Export Plugin Models
"""
from datetime import datetime as _datetime
from frozendict import frozendict as _frozendict
from pytsite import odm_ui as _odm_ui, auth as _auth, odm as _odm, router as _router, widget as _widget, \
    util as _util, form as _form, lang as _lang, auth_storage_odm as _auth_storage_odm
from plugins import content as _content
from . import _widget as _content_export_widget, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ContentExport(_odm_ui.model.UIEntity):
    """oAuth Account Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('driver', required=True))
        self.define_field(_odm.field.Dict('driver_opts'))
        self.define_field(_odm.field.String('content_model', required=True))
        self.define_field(_odm.field.Bool('process_all_authors', default=True))
        self.define_field(_odm.field.Bool('with_images_only', default=True))
        self.define_field(_auth_storage_odm.field.User('owner', required=True))
        self.define_field(_odm.field.Bool('enabled', default=True))
        self.define_field(_odm.field.Integer('errors'))
        self.define_field(_odm.field.String('last_error'))
        self.define_field(_odm.field.Integer('max_age', default=14))
        self.define_field(_odm.field.DateTime('paused_till'))
        self.define_field(_odm.field.List('add_tags'))

    @property
    def driver(self) -> str:
        return self.f_get('driver')

    @property
    def driver_opts(self) -> _frozendict:
        return self.f_get('driver_opts')

    @property
    def content_model(self) -> str:
        return self.f_get('content_model')

    @property
    def owner(self) -> _auth.model.AbstractUser:
        return self.f_get('owner')

    @property
    def process_all_authors(self) -> bool:
        return self.f_get('process_all_authors')

    @property
    def with_images_only(self) -> bool:
        return self.f_get('with_images_only')

    @property
    def enabled(self) -> bool:
        return self.f_get('enabled')

    @property
    def errors(self) -> int:
        return self.f_get('errors')

    @property
    def last_error(self) -> str:
        return self.f_get('last_error')

    @property
    def max_age(self) -> int:
        return self.f_get('max_age')

    @property
    def paused_till(self) -> _datetime:
        return self.f_get('paused_till')

    @property
    def add_tags(self) -> tuple:
        return self.f_get('add_tags')

    @classmethod
    def odm_ui_browser_setup(cls, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.default_sort_field = 'driver'

        browser.data_fields = [
            ('content_model', 'content_export@content_model'),
            ('driver', 'content_export@driver'),
            ('driver_opts', 'content_export@driver_opts'),
            ('process_all_authors', 'content_export@process_all_authors'),
            ('with_images_only', 'content_export@with_images_only'),
            ('max_age', 'content_export@max_age'),
            ('enabled', 'content_export@enabled'),
            ('errors', 'content_export@errors'),
            ('paused_till', 'content_export@paused_till'),
            ('owner', 'content_export@owner')
        ]

    def odm_ui_browser_row(self) -> tuple:
        """Hook.
        """
        driver = _api.get_driver(self.driver)
        content_model = _content.get_model_title(self.content_model)
        driver_desc = _lang.t(driver.get_description())
        opts_desc = driver.get_options_description(self.driver_opts)
        all_authors = '<span class="label label-success">' + self.t('word_yes') + '</span>' \
            if self.process_all_authors else ''
        w_images = '<span class="label label-success">' + self.t('word_yes') + '</span>' \
            if self.with_images_only else ''
        max_age = self.max_age
        enabled = '<span class="label label-success">' + self.t('word_yes') + '</span>' if self.enabled else ''

        if self.errors:
            errors = '<span class="label label-danger" title="{}">{}</span>'\
                .format(_util.escape_html(self.last_error), self.errors)
        else:
            errors = ''

        paused_till = self.f_get('paused_till', fmt='pretty_date_time') if _datetime.now() < self.paused_till else ''

        return content_model, driver_desc, opts_desc, all_authors, w_images, max_age, enabled, \
            errors, paused_till, self.owner.full_name

    def odm_ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        frm.steps = 2

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        if frm.step == 1:
            frm.add_widget(_widget.select.Checkbox(
                weight=10,
                uid='enabled',
                label=self.t('enabled'),
                value=self.enabled,
            ))

            frm.add_widget(_widget.select.Checkbox(
                weight=20,
                uid='process_all_authors',
                label=self.t('process_all_authors'),
                value=self.process_all_authors,
            ))

            frm.add_widget(_widget.select.Checkbox(
                weight=30,
                uid='with_images_only',
                label=self.t('with_images_only'),
                value=self.with_images_only,
            ))

            frm.add_widget(_content.widget.ModelSelect(
                weight=40,
                uid='content_model',
                label=self.t('content_model'),
                value=self.content_model,
                h_size='col-sm-4',
                required=True,
            ))

            frm.add_widget(_content_export_widget.DriverSelect(
                weight=50,
                uid='driver',
                label=self.t('driver'),
                value=self.driver,
                h_size='col-sm-4',
                required=True,
            ))

            frm.add_widget(_widget.input.Integer(
                weight=60,
                uid='max_age',
                label=self.t('max_age'),
                value=self.max_age,
                h_size='col-sm-1',
            ))

            frm.add_widget(_widget.input.Tokens(
                weight=70,
                uid='add_tags',
                label=self.t('additional_tags'),
                value=self.add_tags,
            ))

            frm.add_widget(_widget.select.DateTime(
                weight=80,
                uid='paused_till',
                label=self.t('paused_till'),
                value=self.paused_till,
                h_size='col-sm-5 col-md-4 col-lg-3',
            ))

            frm.add_widget(_widget.input.Integer(
                weight=90,
                uid='errors',
                label=self.t('errors'),
                value=self.errors,
                h_size='col-sm-1',
            ))

        elif frm.step == 2:
            driver = _api.get_driver(_router.request().inp.get('driver'))
            settings_widget = driver.get_settings_widget(self.driver_opts)
            settings_widget.uid = 'driver_opts'
            frm.add_widget(settings_widget)

    def odm_ui_mass_action_entity_description(self) -> str:
        """Get description for mass action form.
        """
        return _api.get_driver(self.driver).get_options_description(self.driver_opts)
