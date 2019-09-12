#!/usr/bin/env python
# coding: utf-8

import os
import logging

from unittest.mock import MagicMock

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.core.option import init
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.controller.project import ScanProject
from seecode_scanner.lib.core.execptions import ScanTemplateNotFound
from seecode_scanner.lib.core.execptions import MissingImportantScanParameters
from seecode_scanner.lib.core.execptions import DistributedConfigurationInvalid


class ScanProjectTestCase(TestCase):

    def setUp(self):
        init()
        self.work_dir = os.path.join(BASEDIR, 'tests', 'data', 'seecode')

    def tearDown(self):
        pass

    def __del__(self):
        try:
            clean_dir(self.work_dir)
        except:
            pass

    def test_online_project_normal(self):
        work_dir = os.path.join(BASEDIR, 'seecode_scanner', 'profiles', 'default.xml')
        # test 1
        scan_parameters = {
            'task_id': 9527,
            'template': "DEFAULT",
            'template_full_path': "template_full_path",
            'threads': '100',
            'work_dir': self.work_dir,
            'project_name': 'seecode ',
            'project_branch': 'master ',
            'project_ssh': 'git@github.com:seecode-audit/seecode-scanner.git',
            'project_web': 'https://github.com/seecode-audit/seecode-scanner',
            'project_type': 'Online',
            'group_name': 'seecode',
            'group_key': 'seecode',
            'log_level': 'info',
            'evidence_start_line_offset': '-5',
            'evidence_count': '100',
        }

        pro = ScanProject(**scan_parameters)
        self.assertTrue(os.path.isdir(pro.scan_path))
        self.assertEqual(pro.scan_path, os.path.join(self.work_dir, 'tasks', str(pro.task_id)))
        self.assertEqual(pro.origin_path, os.path.join(self.work_dir, 'projects', 'seecode'))
        self.assertEqual(pro.log_file, os.path.join(self.work_dir, 'logs', str(pro.task_id), '9527.log'))
        self.assertEqual(pro.log_level, logging.INFO)
        self.assertEqual(pro.type, 'online')
        self.assertEqual(pro.threads, 100)
        self.assertEqual(pro.branch, 'master')
        self.assertEqual(pro.name, 'seecode')
        self.assertEqual(pro.template_name, 'default')
        self.assertEqual(pro.evidence_start_line_offset, -5)
        self.assertEqual(pro.evidence_count, 100)
        self.assertTrue(pro.logger)
        self.assertTrue(pro.task_status)
        self.assertFalse(pro._force_sync_code)
        self.assertFalse(pro.sync_vuln_to_server)

        pro.sync_code = MagicMock(return_value=True)
        pro.sync_code()

    def test_offline_project_normal(self):
        # test 1
        scan_parameters = {
            'task_id': 9528,
            'template': "DEFAULT",
            'work_dir': self.work_dir,
            'project_name': 'seecode ',
            'project_type': 'offline',
            'project_storage_type': 'local',
            'group_name': 'seecode',
            'group_key': 'seecode',
            'log_level': 'debug',
            'force_sync_code': True,
            'sync_vuln_to_server': True,
        }
        with self.assertRaises(MissingImportantScanParameters) as _:
            pro = ScanProject(**scan_parameters)
            self.assertTrue(os.path.isdir(pro.scan_path))
            self.assertEqual(pro.scan_path, os.path.join(self.work_dir, 'tasks', str(pro.task_id)))
            self.assertEqual(pro.origin_path, os.path.join(self.work_dir, 'projects', 'seecode'))
            self.assertEqual(pro.log_level, logging.DEBUG)
            self.assertEqual(pro.type, 'offline')
            self.assertEqual(pro.name, 'seecode')
            self.assertEqual(pro.template_name, 'default')
            self.assertTrue(pro.logger)
            self.assertTrue(pro.task_status)
            self.assertTrue(pro._force_sync_code)
            self.assertTrue(pro.sync_vuln_to_server)

            pro.sync_code = MagicMock(return_value=True)
            pro.sync_code()

    def test_online_project_abnormal(self):
        # test 1
        scan_parameters = {
            'project_type': 'online',
        }

        with self.assertRaises(MissingImportantScanParameters) as _:
            pro = ScanProject(**scan_parameters)

    def test_offline_project_abnormal(self):
        # test 1
        scan_parameters = {
            'template': "DEFAULT",
            'work_dir': self.work_dir,
            'project_name': 'seecode ',
            'project_type': 'offline',
            'project_storage_type': 'ftp',
            'distributed': {
                'ftp': {}
            },
        }
        with self.assertRaises(DistributedConfigurationInvalid) as _:
            ScanProject(**scan_parameters)

        # test 2
        scan_parameters = {
            'template': "DEFAULT",
            'work_dir': self.work_dir,
            'project_name': 'seecode ',
            'project_type': 'offline',
            'project_storage_type': 'LOCAL',
            'distributed': {
                'ftp': {}
            },
        }

        pro = ScanProject(**scan_parameters)
        self.assertEqual(pro._project_storage_type, 'local')

        # test 3
        scan_parameters = {
            'template': "DEFAULT1231",
            'work_dir': self.work_dir,
            'project_name': 'seecode ',
            'project_type': 'offline',
            'project_storage_type': 'local',
            'distributed': {
                'ftp': {}
            },
        }
        with self.assertRaises(ScanTemplateNotFound) as _:
            ScanProject(**scan_parameters)
