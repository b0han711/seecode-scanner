#!/usr/bin/env python
# coding: utf-8

import ast
import os
import tarfile
import glob
import shutil

from seecode_scanner.lib.core.seecode_request import RequestConnect
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.settings import CORE_CONF_FILE
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.core.rsaencrypt import RSAEncrypt
from seecode_scanner.lib.utils.ftpwrapper import FTPWork


class UpgradeManage(object):

    def __init__(self):
        self.server = RequestConnect(
            server_token=conf.server.token
        )

        if not os.path.isfile(CORE_CONF_FILE):
            raise FileNotFoundError(
                'The "seecode_scanner.yml" profile was not found, please confirm that it is configured.'
            )

        self._is_upgrade = False
        self._local_version = None
        self._current_version = None
        self._transport_encryption = False
        self._upgrade_info = {}
        self.rsa = RSAEncrypt()
        if conf.server.public_key_path and conf.server.private_key_path:
            self.rsa.load(conf.server.public_key_path, conf.server.private_key_path)
        self._upgrade_path = os.path.join(paths.UPGRADE_PATH, self.current_version)
        logger.info('Initialize the upgrade environment and create an upgrade directory...')
        make_dir([paths.UPGRADE_PATH, self._upgrade_path])
        self.local_upgrade_file = os.path.join(paths.UPGRADE_PATH, '{0}.tgz'.format(self.current_version))

    def __del__(self):
        clean_dir(paths.UPGRADE_PATH)
        pass

    @property
    def is_upgrade(self):
        if self.current_version:
            logger.info('current version: [v{0}], new version: [v{1}].'.format(self.local_version, self.current_version))
            # TODO self.local_version < self.current_version
            if self.current_version != self.local_version:
                self._is_upgrade = True
        return self._is_upgrade

    @property
    def transport_encryption(self):
        return self._transport_encryption

    @property
    def current_version(self):
        if not self._current_version:
            try:
                logger.info('Check the latest version...')
                url_api = '{0}/api/v2/upgrade/version/'.format(conf.server.domain)
                resp = self.server.get_data(url=url_api)
                if resp and resp['code'] == 200:
                    if 'secret' in resp['data']:
                        logger.info('[+] The server has opened the encrypted communication.')
                        rsa = RSAEncrypt()
                        self._transport_encryption = True
                        decrypt_str = rsa.decrypt_str(resp['data']['secret'])
                        self._upgrade_info = ast.literal_eval(decrypt_str.decode('utf-8'))
                    else:
                        self._upgrade_info = resp['data']
                    self._current_version = self._upgrade_info['version']
                    logger.info('The latest version of: [v{0}]'.format(self._current_version))
            except Exception as ex:
                import traceback;
                traceback.print_exc()
                logger.error(ex)

        return self._current_version

    @property
    def local_version(self):
        if not self._local_version:
            with open(paths.PROFILE_VERSION_PATH, 'rb') as fp:
                self._local_version = fp.read().decode('utf-8')

        return self._local_version

    def upload_upgrade_status_failure(self, reason, stack_trace):
        """

        :param reason:
        :return:
        """
        if self.server:
            url_api = "{0}/api/v2/sys/log/".format(conf.server.domain)
            msg = 'v{0} 升级 v{1} 失败。{2}'.format(self.local_version, self.current_version, reason)
            data = {
                "title": "扫描引擎升级失败",
                "description": msg,
                "stack_trace": stack_trace,
                "level": 1
            }
            self.server.post_data(url=url_api, data=data)

    def upload_upgrade_status_success(self):
        """

        :return:
        """
        if self.server:
            url_api = "{0}/api/v2/sys/log/".format(conf.server.domain)
            msg = 'v{0} 成功升级到 v{1}。'.format(self.local_version, self.current_version)
            data = {
                "title": "扫描引擎升级成功",
                "description": msg,
                "level": 4
            }
            self.server.post_data(url=url_api, data=data)

    def download(self):
        """

        :return:
        """
        # TODO failed try
        logger.info('Start downloading the upgrade package...'.format(self.local_version, self.current_version))
        remote_file = self._upgrade_info['download_path']
        if 'ftp' == self._upgrade_info['download_type'].lower().strip():
            try:
                ftp = FTPWork(
                    host=conf.distributed['ftp']['host'],
                    port=parse_int(conf.distributed['ftp']['port'], 21),
                    username=conf.distributed['ftp']['username'],
                    password=conf.distributed['ftp']['password'],
                    debug=False
                )
                ftp.download_file(self.local_upgrade_file, remote_file)
                return True
            except Exception as ex:
                logger.exception(ex)
        elif 'aws' == self._upgrade_info['download_type'].lower().strip():
            pass  # TODO
        return False

    def start_upgrade(self):
        """

        :return:
        """
        try:
            logger.info('Start upgrading, check if the local version is consistent with the server version...')
            if self.is_upgrade:
                self.download()
                if os.path.isfile(self.local_upgrade_file):
                    logger.info('Start decompressing the encryption upgrade package...')
                    # Decrypted encrypted upgrade package
                    tar = tarfile.open(self.local_upgrade_file, 'r:gz')
                    file_names = tar.getnames()
                    for file_name in file_names:
                        tar.extract(file_name, self._upgrade_path)
                    tar.close()
                    file_list = glob.glob(os.path.join(self._upgrade_path, '*.bin'))
                    save_tgz = ''
                    for l in file_list:
                        file_name = os.path.splitext(os.path.basename(l))[0]
                        save_tgz = os.path.join(self._upgrade_path, '{0}.tgz'.format(file_name))
                        self.rsa.decrypt_file(l, save_tgz)
                        break
                    logger.info('Unzip the encryption upgrade package to complete.')

                    # Decompress and decrypt the compressed package
                    if os.path.isfile(save_tgz):
                        logger.info('Start decompressing the decryption upgrade package...')
                        decrypt_path = os.path.join(self._upgrade_path, 'decrypt')
                        tar = tarfile.open(save_tgz, 'r:gz')
                        file_names = tar.getnames()
                        for file_name in file_names:
                            tar.extract(file_name, decrypt_path)
                        tar.close()

                        logger.info('Decompression and decryption upgrade package completed')

                        logger.info('Start syncing scan templates...')
                        # profiles
                        profiles = glob.glob(os.path.join(decrypt_path, '*.xml'))
                        for p in profiles:
                            file_name = os.path.basename(p)
                            dest = os.path.join(paths.ROOT_PROFILE_PATH, file_name)
                            if os.path.isfile(dest):
                                os.unlink(dest)
                            shutil.copy(p, dest)
                        logger.info('Synchronous scan template completion.')
                        # plugins
                        blacklist_path = os.path.join(decrypt_path, 'plugins', 'blacklist')
                        if os.path.isdir(blacklist_path):
                            logger.info('Start syncing blacklist plugin...')
                            clean_dir(paths.ROOT_PLUGINS_BLACKLIST_PATH)
                            shutil.copytree(blacklist_path, paths.ROOT_PLUGINS_BLACKLIST_PATH)
                            logger.info('Synchronous blacklist plugin completed.')
                        whitelist_path = os.path.join(decrypt_path, 'plugins', 'whitelist')
                        if os.path.isdir(whitelist_path):
                            logger.info('Start syncing whitelist plugin...')
                            clean_dir(paths.ROOT_PLUGINS_WHITELIST_PATH)
                            shutil.copytree(whitelist_path, paths.ROOT_PLUGINS_WHITELIST_PATH)
                            logger.info('Synchronous whitelist plugin completed.')

                        for d in [paths.ROOT_PLUGINS_BLACKLIST_PATH, paths.ROOT_PLUGINS_WHITELIST_PATH]:
                            module_file = os.path.join(d, '__init__.py')
                            if not os.path.isfile(module_file):
                                with open(module_file, 'wb') as fp:
                                    fp.write(''.encode('utf-8'))

                    # write version
                    logger.info('Start updating the current version to v{0}.'.format(self.current_version))
                    with open(paths.PROFILE_VERSION_PATH, 'wb') as fp:
                        fp.write(self.current_version.encode("utf-8"))
                    self.upload_upgrade_status_success()
                    logger.info('Upgrade completed, current version: v{0}'.format(self.current_version))
                else:
                    self.download()
                    logger.error('Download upgrade package failed, "{0}" not found.'.format(self._upgrade_info['download_path']))
            else:
                logger.info('[*] No upgrade required, exit the upgrade program.')
        except Exception as ex:
            import traceback
            self.upload_upgrade_status_failure(reason=str(ex), stack_trace=traceback.format_exc())
            logger.critical(ex)
