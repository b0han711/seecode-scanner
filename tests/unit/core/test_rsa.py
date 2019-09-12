#!/usr/bin/env python
# coding: utf-8
import os

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.core.rsaencrypt import RSAEncrypt
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class RSATestCase(TestCase):

    def setUp(self):
        self.work_dir = os.path.join(BASEDIR, 'tests', 'data', 'tmp')
        make_dir(self.work_dir)

    def tearDown(self):
        pass

    def __del__(self):
        try:
            clean_dir(self.work_dir)
        except:
            pass

    def test_encrypt_decrypt_str(self):
        rsa = RSAEncrypt()
        message = 's' * 2048
        # test encrypt
        crypto_content = rsa.encrypt_str(message)
        self.assertIsNotNone(crypto_content)

        # test decrypt
        content = rsa.decrypt_str(crypto_content)
        self.assertEqual(message, content.decode('utf-8'))

        # test sign
        hash_method = 'SHA-512'
        signature = rsa.sign(message, hash_method)
        self.assertIsNotNone(message)

        # test verify
        self.assertTrue(rsa.verify(message, signature, hash_method))

    def test_encrypt_decrypt_file(self):
        # test encrypt
        rsa = RSAEncrypt()
        file_content = 'Seecode encrypted file test.'
        encrypt_file_path = os.path.join(self.work_dir, 'test.txt')
        with open(encrypt_file_path, 'wb+') as fp:
            fp.write(file_content.encode('utf-8'))
        self.assertTrue(os.path.isfile(encrypt_file_path))
        cfp = rsa.encrypt_file(encrypt_file_path)
        self.assertTrue(os.path.isfile(cfp))
        with open(cfp, 'rb') as fp:
            content = fp.read()
            self.assertNotEqual(content.decode('utf-8'), file_content)
        # test decrypt
        decrypt_file_path = os.path.join(self.work_dir, 'test1.txt')
        rsa.decrypt_file(cfp, save_path=decrypt_file_path)
        self.assertTrue(os.path.isfile(decrypt_file_path))
        with open(decrypt_file_path, 'rb') as fp:
            content = fp.read()
            self.assertEqual(content.decode('utf-8'), file_content)

    def test_generate_pem(self):
        rsa = RSAEncrypt()
        g, s = rsa.generate_pem(self.work_dir)

        self.assertTrue(os.path.join(g))
        self.assertTrue(os.path.join(s))
