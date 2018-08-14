import boto3
import os
import logging
import operator
from urllib.parse import urlparse
from io import BytesIO

log = logging.getLogger('rds-log')

rds = boto3.client('rds')
s3 = boto3.resource('s3')

def process(db_identifier, target_path):
    result = rds.describe_db_log_files(DBInstanceIdentifier=db_identifier)
    rds_logs = sorted((rds_log for rds_log in result['DescribeDBLogFiles']),
                        key=operator.itemgetter('LogFileName'))
    #print(rds_logs)
    parsed = urlparse(target_path)
    prefix = parsed.path
    if prefix.startswith('/'):
        prefix = prefix[1:]
    bucketname = parsed.netloc
    bucket = s3.Bucket(bucketname)
    files = bucket.objects.filter(Prefix=prefix)
    existing = {}
    for f in files:
        existing[f.key] = f.size
    for rds_log in rds_logs:
        log_filename = rds_log['LogFileName']
        key = os.path.join(prefix, log_filename)
        if existing.get(key, 0) != rds_log['Size']:
            log.info('Fetching log file {}'.format(log_filename))
            data = ""
            pending = True
            marker = '0'
            while pending:
                log.info('Request: {name} ({marker})'.format(name=log_filename, marker=marker))
                response = rds.download_db_log_file_portion(
                    DBInstanceIdentifier=db_identifier,
                    LogFileName=log_filename,
                    NumberOfLines=100, # lines small so big queries don't get truncated
                    Marker=marker
                )
                data += response.get('LogFileData')
                marker = response.get('Marker')
                pending = response.get('AdditionalDataPending')
            bucket.upload_fileobj(
                BytesIO(data.encode()),
                key,
                {
                    'ServerSideEncryption': 'AES256',
                }
            )
        else:
            log.info('Skipping already saved file {}'.format(log_filename))
