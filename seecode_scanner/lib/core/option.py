# encoding: utf-8

import os
import glob
import logging

from seecode_scanner import __version__
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.datatype import AttribDict
from seecode_scanner.lib.core.common import checkFile
from seecode_scanner.lib.parse.configfile import configFileParser
from seecode_scanner.lib.parse.configfile import configCoreFileParser
from seecode_scanner.lib.controller.profile import ScanProfile
from seecode_scanner.lib.core.settings import CORE_CONF_FILE


def _init_paths():
    """
    初始化路径
    :return:
    """
    paths.ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    paths.ROOT_WORK_PATH = '/data/seecode/'
    paths.ROOT_CONF_PATH = '/usr/local/etc/seecode/'
    paths.ROOT_CONFIG_PATH = os.path.join(paths.ROOT_CONF_PATH, 'conf')
    paths.ROOT_PROFILE_PATH = os.path.join(paths.ROOT_PATH, 'profiles')
    paths.ROOT_PLUGINS_PATH = os.path.join(paths.ROOT_PATH, 'plugins')
    paths.ROOT_PLUGINS_BLACKLIST_PATH = os.path.join(paths.ROOT_PLUGINS_PATH, 'blacklist')
    paths.ROOT_PLUGINS_WHITELIST_PATH = os.path.join(paths.ROOT_PLUGINS_PATH, 'whitelist')
    paths.SERVICES_FILE = os.path.join(paths.ROOT_CONFIG_PATH, 'services.json')
    paths.PROFILE_VERSION_PATH = os.path.join(paths.ROOT_PROFILE_PATH, 'version.txt')
    paths.UPGRADE_PATH = os.path.join(paths.ROOT_PATH, 'upgrades')


def setVerbosity():
    """
    This function set the verbosity of output messages.
    :return:
    """
    if conf.scan.log_level == 'error':
        logger.setLevel(logging.ERROR)
    elif conf.scan.log_level == 'warn':
        logger.setLevel(logging.WARN)
    elif conf.scan.log_level == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def _setConfAttributes():
    """
    This function set some needed attributes into the configuration
    singleton.
    """

    conf.general.version = __version__


def init_kb(**kwargs):
    """

    :return:
    """
    _setConfAttributes()
    project_key = kwargs.get("project_key")
    if project_key:
        kb.result[project_key] = {}


def _mergeOptions(inputOptions, conf):
    """
    Merge command line options with configuration file and default options.
    @param inputOptions: optparse object with command line options.
    @type inputOptions: C{instance}
    """

    if inputOptions.config:
        configFileParser(inputOptions.config)

    conf.general.is_test = inputOptions.enable_test_services
    conf.general.config = inputOptions.config
    conf.general.enable_upgrade = inputOptions.enable_upgrade

    conf.celery.enable = inputOptions.enable_celery
    conf.celery.concurrency = inputOptions.celery_concurrency
    conf.celery.name = inputOptions.celery_name

    # agent
    conf.agent.enable_monitor = inputOptions.enable_monitor

    # scan
    conf.scan.template = conf.scan.template or inputOptions.template
    if not any((conf.agent.enable_monitor, conf.agent.enable_upgrade, )):
        if conf.scan.template_full_path:
            checkFile(conf.scan.template_full_path)
        else:
            checkFile('{0}.xml'.format(os.path.join(paths.ROOT_PROFILE_PATH, conf.scan.template)))

    conf.scan.template = conf.scan.template or inputOptions.template
    conf.scan.threads = conf.scan.threads or inputOptions.threads
    conf.scan.work_dir = conf.scan.work_dir or paths.ROOT_WORK_PATH
    conf.scan.project_path = conf.scan.project_path or inputOptions.project_path
    conf.scan.project_name = conf.scan.project_name or inputOptions.project_name
    conf.scan.result_file = conf.scan.result_file or inputOptions.result_file
    conf.scan.log_level = conf.scan.log_level or inputOptions.verbose

    if conf.scan.project_path and conf.scan.project_path.startswith('./'):
        conf.scan.project_path = os.path.join(os.getcwd(), conf.scan.project_path[2:])



def _mergeCoreOptions(configFile):
    """
    """
    if configFile:
        configCoreFileParser(configFile)


def initOptions(inputOptions, overrideOptions):
    _setConfAttributes()
    _mergeOptions(inputOptions, overrideOptions)


def load_scan_template(template_file_path=None):
    """

    :return:
    """
    if template_file_path and os.path.isfile(template_file_path):
        profile = ScanProfile(profile_path=template_file_path)
        if profile and profile.name not in kb.profiles:
            kb.profiles[profile.name] = profile
    else:
        file_list = glob.glob(os.path.join(paths.ROOT_PROFILE_PATH, "*.xml"))
        for item in file_list:
            profile = ScanProfile(profile_path=item)
            if profile and profile.name not in kb.profiles:
                kb.profiles[profile.name] = profile


def init():
    """
    Set attributes into both configuration and knowledge base singletons
    based upon command line and configuration file options.
    """

    _init_paths()
    _setConfAttributes()
    setVerbosity()
    _mergeCoreOptions(CORE_CONF_FILE)
