import logging
import rollbar
import rollbar.logger
import click
from rds_log import settings

class DataFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, 'data'):
            record.data = ''
        else:
            record.data = '\n' + str(record.data)
        return True


def setup(loglevel):
    f = DataFilter()

    log = logging.getLogger()
    log.setLevel(getattr(logging, loglevel))
    local_logger = logging.StreamHandler()
    local_logger.setLevel(getattr(logging, loglevel))
    # add formatter to local_logger
    local_logger.setFormatter(logging.Formatter('%(name)s %(levelname)s %(message)s %(data)s'))
    local_logger.addFilter(f)
    log.addHandler(local_logger)


    if settings.ROLLBAR_API_KEY:
        notify_log = logging.getLogger('notify')
        rollbar.init(
            settings.ROLLBAR_API_KEY,
            settings.ROLLBAR_ENVIRONMENT,
            scrub_fields=settings.ROLLBAR_SCRUB_FIELDS,
        )
        # Send to rollbar all WARNING or higher logs
        rollbar_warn_logger = rollbar.logger.RollbarHandler()
        rollbar_warn_logger.setLevel(logging.WARNING)
        rollbar_warn_logger.addFilter(f)
        log.addHandler(rollbar_warn_logger)

        # Send to rollbar INFO or higher logs only from separate logger
        rollbar_info_logger = rollbar.logger.RollbarHandler()
        rollbar_info_logger.setLevel(logging.INFO)
        rollbar_info_logger.addFilter(f)
        notify_log.addHandler(rollbar_info_logger)
    else:
        log.warning('No Rollbar Api Key, logging locally only')


def loglevel_option(f):
    def callback(ctx, param, value):
        setup(value.upper())
    return click.option(
        '--loglevel',
        envvar='LOGLEVEL',
        default='INFO',
        help='Set print log statements level',
        callback=callback
    )(f)
