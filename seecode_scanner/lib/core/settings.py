# coding: utf-8

import platform
import time
import os

from seecode_scanner import __version__

VERSION_STRING = "\033[42;37m SeeCode Audit \033[0m seecode-scanner/" \
                 "%s%s" % (__version__, "-%s" % time.strftime("%Y%m%d", time.gmtime(os.path.getctime(__file__))))
DESCRIPTION = "SeeCode Audit Scanner"

IS_WIN = platform.system() == 'Windows'

# HTTP
USER_AGENT = 'SeeCode Audit Scanner v{0} bot'.format(__version__)


# Core
CORE_CONF_FILE = ''
CORE_CONF_SEARCH_PATH = ('/usr/local/etc/seecode/conf/', '/etc/')

for c in CORE_CONF_SEARCH_PATH:
    f = os.path.join(c, 'seecode_scanner.yml')
    if os.path.isfile(f):
        CORE_CONF_FILE = f

# sonar
SONAR_PROJECT_PROPERTIES = """sonar.projectKey={{project_key}}
sonar.projectName={{project_name}}
sonar.projectVersion=1.0
sonar.sources=.
sonar.sourceEncoding=UTF-8
sonar.exclusions=**/node_modules/**/*.*,
sonar.host.url={{sonar_host}}
sonar.login={{sonar_login}}
sonar.java.binaries=."""

BASIC_SCOPE = {
    'vulnerability': {
        'basic': 300.0,
        '1': {
            'scope': 0.4,
            'min': 75.0,
            'max': 100.0,
        },
        '2': {
            'scope': 0.3,
            'min': 50.0,
            'max': 75.0,
        },
        '3': {
            'scope': 0.2,
            'min': 25.0,
            'max': 50.0,
        },
        '4': {
            'scope': 0.1,
            'min': 0.0,
            'max': 25.0,
        },
    },
    'bug': {
        'basic': 200.0,
        '1': {
            'scope': 0.4,
            'min': 75.0,
            'max': 100.0,
        },
        '2': {
            'scope': 0.3,
            'min': 50.0,
            'max': 75.0,
        },
        '3': {
            'scope': 0.2,
            'min': 25.0,
            'max': 50.0,
        },
        '4': {
            'scope': 0.1,
            'min': 0.0,
            'max': 25.0,
        },
    },
    'code smell': {
        'basic': 100.0,
        '1': {
            'scope': 0.1,
            'min': 0.0,
            'max': 25.0,
        },
        '2': {
            'scope': 0.2,
            'min': 25,
            'max': 50,
        },
        '3': {
            'scope': 0.3,
            'min': 50.0,
            'max': 75.0,
        },
        '4': {
            'scope': 0.4,
            'min': 75.0,
            'max': 100.0,
        },
    }
}
