# coding:utf-8

import yaml
import os
import json
import rsa

from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.common import checkFile

config = None


def configFileParser(configFile):
    """
    Parse configuration file and save settings into the configuration
    advanced dictionary.
    """
    global config
    
    debugMsg = "parsing configuration file"
    logger.debug(debugMsg)

    checkFile(configFile)
    with open(configFile, 'rb') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

    if not config.get("scan"):
        errMsg = "missing a mandatory section 'Scan' in the configuration file"
        raise Exception(errMsg)

    conf.scan.update(config['scan'])
    if 'Distributed' in config:
        conf.distributed.update(config['Distributed'])


def configCoreFileParser(configFile):
    """
    Parse configuration file and save settings into the configuration
    advanced dictionary.
    """
    
    debugMsg = "parsing configuration core file"
    logger.debug(debugMsg)

    checkFile(configFile)
    with open(configFile, 'rb') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

    if not config.get("server"):
        errMsg = "missing a mandatory section 'server' in the configuration file"
        raise Exception(errMsg)

    conf.server.update(config['server'])
    conf.http.update(config['http'])
    conf.celery.update(config['celery'])
    conf.distributed.update(config['distributed'])

    if config['http']:
        for k, v in config['http'].items():
            if k == 'user-agent':
                conf.http.headers['User-Agent'] = config['http']['user-agent'].replace('%VERSION%', conf.general.version)
                del conf.http['user-agent']
            elif k == 'proxies':
                conf.http.proxies = {}
                for proxy_type, proxy_value in config['http']['proxies'].items():
                    if proxy_value:
                        conf.http.proxies[proxy_type] = proxy_value

    if conf.server.domain:
        conf.agent.monitor_url = '{0}{1}node/host/'.format(conf.server.domain, conf.server.api_uri)
        conf.agent.upgrade_url = '{0}{1}upgrade/'.format(conf.server.domain, conf.server.api_uri)
        conf.agent.task_url = '{0}{1}client/task/'.format(conf.server.domain, conf.server.api_uri)

    if os.path.isfile(paths.SERVICES_FILE):
        with open(paths.SERVICES_FILE, "rb") as fp:
            conf.general.services = json.load(fp)

    if conf.server.public_key_path:
        try:
            with open(conf.server.public_key_path, 'r') as fp:
                conf.server.pubkey = rsa.PublicKey.load_pkcs1(fp.read().encode())
        except Exception as ex:
            logger.warn(ex)
