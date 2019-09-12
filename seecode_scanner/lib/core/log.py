#!/usr/bin/env python
# coding:utf-8

import logging
import sys

logger = logging.getLogger(__name__)

try:
    from seecode_scanner.lib.core.ansistrm import ColorizingStreamHandler
    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER_INFO = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
FORMATTER_DEV = logging.Formatter("[%(asctime)s] [%(pathname)s(%(lineno)d)%(funcName)s()] [%(levelname)s] %(message)s", "%H:%M:%S")

# info
LOGGER_HANDLER.setFormatter(FORMATTER_INFO)
logger.setLevel(logging.INFO)

# debug
# LOGGER_HANDLER.setFormatter(FORMATTER_DEV)
# logger.setLevel(logging.DEBUG)

logger.addHandler(LOGGER_HANDLER)