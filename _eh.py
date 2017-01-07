"""PytSite Content Export Event Handlers.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import reg as _reg, odm as _odm, logger as _logger
from plugins import content as _content
from . import _error, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_1min():
    """'pytsite.cron.1min' event handler.
    """
    max_errors = _reg.get('content_export.max_errors', 13)
    delay_errors = _reg.get('content_export.delay_errors', 120)

    exporters_f = _odm.find('content_export') \
        .eq('enabled', True) \
        .lt('paused_till', _datetime.now()) \
        .sort([('errors', _odm.I_ASC)])

    # It has no sense to cache such queries because argument is different every time
    exporters_f.cache(0)

    for exporter in exporters_f.get():
        # Search for content entities which are hasn't been exported yet
        content_f = _content.find(exporter.content_model) \
            .gte('publish_time', _datetime.now() - _timedelta(exporter.max_age)) \
            .ninc('options.content_export', [str(exporter.id)]) \
            .sort([('publish_time', _odm.I_ASC)])

        # Get content only with images
        if exporter.with_images_only:
            content_f.ne('images', [])

        # Filter by content owner
        if not exporter.process_all_authors:
            content_f.eq('author', exporter.owner.uid)

        for entity in content_f.get():
            try:
                exporter.lock()

                driver = _api.get_driver(exporter.driver)

                msg = "Content export started. Model: '{}', title: '{}', driver: '{}', options: '{}'" \
                    .format(entity.model, entity.title, exporter.driver,
                            driver.get_options_description(exporter.driver_opts))
                _logger.info(msg)

                # Ask driver to perform export
                driver.export(entity=entity, exporter=exporter)

                # Saving information that entity was exported
                with entity:
                    entity_opts = dict(entity.options)
                    if 'content_export' not in entity_opts:
                        entity_opts['content_export'] = []
                    entity_opts['content_export'].append(str(exporter.id))
                    entity.f_set('options', entity_opts)
                    entity.save()

                # Reset errors count to zero after each successful export
                if exporter.errors:
                    exporter.f_set('errors', 0)

            except _error.ExportError as e:
                # Increment errors counter
                exporter.f_inc('errors')

                # Store info about error
                exporter.f_set('last_error', str(e))
                _logger.error(str(e), exc_info=e, stack_info=True)

                if exporter.errors >= max_errors:
                    # Disable if maximum errors count reached
                    exporter.f_set('enabled', False)
                else:
                    # Pause exporter
                    exporter.f_set('paused_till', _datetime.now() + _timedelta(minutes=delay_errors))

                # Stop iterating over entities and go on with new exporter
                break

            finally:
                exporter.save().unlock()
