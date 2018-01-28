from __future__ import absolute_import, unicode_literals

import os
import logging

from local_config import *

assert SENDER_EMAIL and SENDER_PASSWORD, 'Please configure local_config with SENDER_EMAIL and SENDER_PASSWORD'

RECIPIENT = 'ddmilanpp@gmail.com'
SEND_EMAIL = os.environ.get('SEND_EMAIL', True)
OUTPUT_FILE = os.environ.get('OUTPUT', 'timeout_output.html')
LOG_LEVEL = logging.INFO
