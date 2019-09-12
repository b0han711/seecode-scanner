#!/usr/bin/env python
# coding: utf-8
import os
import time

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.utils.ftpwrapper import FTPWork
from seecode_scanner.lib.core.common import hash_md5
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class FTPWorkTestCase(TestCase):
    host = os.getenv("SEECODE_FTP_HOST", '192.168.56.1')
    port = os.getenv("SEECODE_FTP_PORT", 21)
    username = os.getenv("SEECODE_FTP_USER", "ftp")
    password = os.getenv("SEECODE_FTP_PWD", '1qaz!QAZ')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_dir(self):
        ftp = FTPWork(
            host=FTPWorkTestCase.host,
            port=FTPWorkTestCase.port,
            username=FTPWorkTestCase.username,
            password=FTPWorkTestCase.password,
        )
        test_dir = '/test_seecode'
        self.assertTrue(ftp.make_dir(test_dir))
        self.assertTrue(ftp.check_dir_exists(test_dir))
        self.assertTrue(ftp.remove_dir(test_dir))

    def test_upload_file_and_download_file(self):
        file_name = '{0}.txt'.format(hash_md5('{0}'.format(time.time())))
        file_path = os.path.join(BASEDIR, 'tests', 'data', 'tmp', file_name)
        file_content = 'ftp test.'
        make_dir(os.path.join(BASEDIR, 'tests', 'data', 'tmp'))
        with open(file_path, 'wb') as fp:
            fp.write(file_content.encode('utf-8'))
        self.assertTrue(os.path.isfile(file_path))

        ftp = FTPWork(
            host=FTPWorkTestCase.host,
            port=FTPWorkTestCase.port,
            username=FTPWorkTestCase.username,
            password=FTPWorkTestCase.password,
        )
        # test upload
        self.assertTrue(ftp.upload_file(file_path, file_name))
        # test download
        save_file_local_path = os.path.join(BASEDIR, 'tests', 'data', 'tmp', 'ftp_download.txt')
        ftp.download_file(save_file_local_path, file_name)
        self.assertTrue(os.path.isfile(save_file_local_path))
        with open(file_path, 'rb') as fp:
            c = fp.read()
            self.assertEqual(file_content, c.decode('utf-8'))
        # test delete
        self.assertTrue(ftp.delete_file(file_name))

        clean_dir(os.path.join(BASEDIR, 'tests', 'data', 'tmp'))
