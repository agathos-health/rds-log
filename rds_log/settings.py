import os

ROLLBAR_API_KEY = os.environ.get(
    'ROLLBAR_API_KEY',
    default=''
)
ROLLBAR_ENVIRONMENT = os.environ.get(
    'ROLLBAR_ENVIRONMENT',
    default='development'
)
