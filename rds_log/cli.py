# -*- coding: utf-8 -*-

"""Console script for rds_log."""
import sys
import logging
import click

from rds_log import logger, processor

log = logging.getLogger('consolidate')
notify_log = logging.getLogger('notify')

@click.command()
@click.argument(
    'db_identifier',
    required=True
)
@click.argument(
    'target_path',
    required=True
)
@logger.loglevel_option
def main(db_identifier, target_path, **kwargs):
    processor.process(db_identifier, target_path)
    notify_log.info('DB log consolidated.')
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)
        sys.exit(1)
