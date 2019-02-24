"""This logger is setup to replace the default logging, so that all
custom logging is stored in json format.

Example:
    Code:
        logger.info('Event Action')

    Default output:
        [INFO]  2019-01-22 11:53:42,670Z    5e2ae11b-0dd3-4c5b-8d84-bdfb3dc1a5a2'    Event Action

    Logger output:
        {
            "levelname": "INFO",
            "asctime": "2019-01-01 00:00:00,000",
            "msecs": 500.0000000000000,
            "aws_request_id": "5e2ae11b-0dd3-4c5b-8d84-bdfb3dc1a5a2'",
            "message": "Event Action"
        }
"""

import logging
import os

from pythonjsonlogger import jsonlogger

from src.common.exceptions import InvalidLogLevel

# This is the default pattern aws lambdas use,
# so all logging information is available in json object.
pattern = "[%(levelname)-8s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(message)s\n"
logger = logging.getLogger()
formatter = jsonlogger.JsonFormatter(pattern)
for h in logger.handlers:
    h.setFormatter(formatter)

log_level = os.environ.get("LOG_LEVEL", "INFO")
log_values = [name for name in logging._levelToName.values()]
if log_level not in log_values:
    message = f"Invalid log level set: {log_level}"
    raise InvalidLogLevel(message)

logger.setLevel(log_level)
