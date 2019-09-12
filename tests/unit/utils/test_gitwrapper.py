#!/usr/bin/env python
# coding: utf-8
import os
from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.utils.gitwrapper import GitOperator
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir


class GitOperatorTestCase(TestCase):
    work_dir = os.path.join(BASEDIR, 'tests', 'data', 'test_git')
    ssh_url = 'git@github.com:seecode-audit/vuln_java.git'

    def setUp(self):
        pass

    def tearDown(self):
        clean_dir(GitOperatorTestCase.work_dir)

    def test_file_exists_in_repo(self):
        git = GitOperator(
            project_path=GitOperatorTestCase.work_dir,
            git_url=GitOperatorTestCase.ssh_url
        )
        git.checkout_branch_sync_code("master")
        self.assertTrue(git.file_exists_in_repo('pom.xml'))

    def test_checkout_file_and_all(self):
        # test checkout file
        git = GitOperator(
            project_path=GitOperatorTestCase.work_dir,
            git_url=GitOperatorTestCase.ssh_url
        )
        # test checkout_branch_sync_code
        git.checkout_branch_sync_code("master")
        file_path = os.path.join(GitOperatorTestCase.work_dir, 'pom.xml')
        self.assertTrue(os.path.isfile(file_path))
        os.unlink(file_path)
        self.assertFalse(os.path.isfile(file_path))
        git.checkout_file('pom.xml')
        self.assertTrue(os.path.isfile(file_path))

        # test get_branch_last_commit_id
        self.assertIsNotNone(git.get_branch_last_commit_id())

        # test get_commit_author
        self.assertIsNotNone(git.get_commit_author('pom.xml'))

        # test get_current_branch
        self.assertEqual(git.get_current_branch(), 'master')
