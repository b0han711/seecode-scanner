#!/usr/bin/env python
# coding: utf-8

from unittest.mock import MagicMock

from tests.unit.common import TestCase

from seecode_scanner.lib.controller.task import TaskStatus


class TaskStatusTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_initialization(self):
        task = TaskStatus()
        task.update_initialization = MagicMock(return_value=True)
        self.assertTrue(task.update_initialization("初始化扫描项目"))
        self.assertIsNotNone(task.executor_ip)
        self.assertIsNotNone(task.start_time)
        self.assertIsNone(task.task_id)

    def test_update_statistics(self):
        task = TaskStatus()
        task.update_statistics = MagicMock(return_value=True)
        self.assertTrue(task.update_statistics("分析项目组件"))

    def test_update_scanning(self):
        task = TaskStatus()
        task.update_scanning = MagicMock(return_value=True)
        self.assertTrue(task.update_scanning("开始扫描"))

    def test_update_complete(self):
        task = TaskStatus()
        task.update_complete = MagicMock(return_value=True)
        self.assertTrue(task.update_complete("扫描完成"))

    def test_update_failed(self):
        task = TaskStatus()
        task.update_failed = MagicMock(return_value=True)
        self.assertTrue(task.update_failed("扫描失败"))

    def test_bulk_send_component(self):
        task = TaskStatus()
        task.bulk_send_component = MagicMock(return_value=True)
        self.assertTrue(task.bulk_send_component([]))

    def test_bulk_send_vulnerability(self):
        task = TaskStatus()
        task.bulk_send_vulnerability = MagicMock(return_value=True)
        self.assertTrue(task.bulk_send_vulnerability([]))
