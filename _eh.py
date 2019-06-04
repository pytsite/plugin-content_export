"""PytSite Content Export Plugin Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime, timedelta
from pytsite import reg, logger, cache
from plugins import content, odm, auth
from . import _error
from ._api import get_driver

_MAX_ERRORS = reg.get('content_export.max_errors', 13)
_DELAY_ERRORS = reg.get('content_export.delay_errors', 120)
_CACHE = cache.create_pool('content_export')


def cron_1min():
    """'pytsite.cron.1min' event handler.
    """
    if _CACHE.has('working'):
        logger.warn('Another instance of content export is currently working')
        return

    _CACHE.put('working', True, 600)

    exporters_f = odm.find('content_export') \
        .eq('enabled', True) \
        .lt('paused_till', datetime.now()) \
        .sort([('errors', odm.I_ASC)])

    # It has no sense to cache such queries because argument is different every time
    exporters_f.cache(0)

    for exporter in exporters_f.get():
        # Search for content entities which are hasn't been exported yet
        content_f = content.find(exporter.content_model, language='*') \
            .gte('publish_time', datetime.now() - timedelta(exporter.max_age)) \
            .ninc('options.content_export', [str(exporter.id)]) \
            .sort([('publish_time', odm.I_ASC)])

        # Get content only with images
        if exporter.with_images_only:
            content_f.ne('images', [])

        # Filter by content owner
        if not exporter.process_all_authors:
            content_f.eq('author', exporter.owner.uid)

        for entity in content_f.get():
            try:
                driver = get_driver(exporter.driver)

                msg = "Content export started. Model: '{}', title: '{}', driver: '{}', options: '{}'" \
                    .format(entity.model, entity.title, exporter.driver,
                            driver.get_options_description(exporter.driver_opts))
                logger.info(msg)

                # Ask driver to perform export
                driver.export(entity=entity, exporter=exporter)

                # Update information that entity was exported
                entity_opts = dict(entity.options)
                if 'content_export' not in entity_opts:
                    entity_opts['content_export'] = []
                entity_opts['content_export'].append(str(exporter.id))
                entity.f_set('options', entity_opts)

                # Save exported entity
                try:
                    auth.switch_user_to_system()
                    entity.save()
                finally:
                    auth.restore_user()

                # Reset errors count to zero after each successful export
                if exporter.errors:
                    exporter.f_set('errors', 0)

            except _error.ExportError as e:
                # Increment errors counter
                exporter.f_inc('errors')

                # Store info about error
                exporter.f_set('last_error', str(e))
                logger.error(e)

                if exporter.errors >= _MAX_ERRORS:
                    # Disable if maximum errors count reached
                    exporter.f_set('enabled', False)
                else:
                    # Pause exporter
                    exporter.f_set('paused_till', datetime.now() + timedelta(minutes=_DELAY_ERRORS))

                # Save exporter
                try:
                    auth.switch_user_to_system()
                    exporter.save()
                finally:
                    auth.restore_user()

                # Stop iterating over entities and go on with new exporter
                break

    _CACHE.rm('working')
