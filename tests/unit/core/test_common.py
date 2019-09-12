#!/usr/bin/env python
# coding: utf-8
import os

from tests.unit.common import TestCase
from tests.unit.common import BASEDIR

from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import parse_bool
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.core.common import get_localhost_ip
from seecode_scanner.lib.core.common import check_ip
from seecode_scanner.lib.core.common import get_dir_size
from seecode_scanner.lib.core.common import get_risk_by_severity
from seecode_scanner.lib.core.common import get_issue_type_by_sonar
from seecode_scanner.lib.core.common import get_total_page
from seecode_scanner.lib.core.common import str_to_list
from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.core.common import checkFile


class CommonTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exec_cmd(self):
        # test 1
        cmd1 = ['echo', '"test_exec_cmd"']
        output, err = exec_cmd(' '.join(cmd1))
        self.assertTrue("test_exec_cmd\n" == output.decode("utf-8"))
        # test 2
        cmd1 = ['not_exists_cmd', '"test_exec_cmd"']
        output, err = exec_cmd(' '.join(cmd1))
        self.assertEqual('', output.decode("utf-8"))
        self.assertIn('command not found', err.decode("utf-8"))

    def test_parse_int(self):
        # test 1
        list_of_var1 = ['1', 0x1, b'1']
        for i in list_of_var1:
            self.assertTrue(parse_int(i) == 1)

        list_of_var2 = ['abcd', type(int)]
        for i in list_of_var2:
            self.assertTrue(parse_int(i) == 0)

    def test_parse_int_or_str(self):
        # test 1
        list_of_var1 = ['1', 0x1, b'1']
        for i in list_of_var1:
            # print('******', i, parse_int_or_str(i))
            self.assertTrue(parse_int_or_str(i) == 1)
        # test 2
        list_of_var2 = ['abcd', b'abcd ']
        for i in list_of_var2:
            # print('******', i, parse_int_or_str(i), type(i))
            self.assertTrue(parse_int_or_str(i) == 'abcd')
        # test 3
        list_of_var3 = [type(os), type(int)]
        for i in list_of_var3:
            # print('******', i, parse_int_or_str(i), type(i))
            self.assertEqual(parse_int_or_str(i), None)

    def test_parse_bool(self):
        # test 1
        list_of_var1 = ['1 ', 1, b'1 ', True, 'true ', 0xabc]
        for i in list_of_var1:
            # print('******', i, parse_bool(i))
            self.assertEqual(parse_bool(i), True)
        # test 2
        list_of_var2 = ['false', b'False ', False,  '', None, 0, 'admin']
        for i in list_of_var2:
            # print('******', i, parse_bool(i))
            self.assertEqual(parse_bool(i), False)

    def test_make_dir(self):
        # test1
        dir_list = ['/tmp/t/1', ['/tmp/t/2', '/tmp/t/3']]
        for i in dir_list:
            if isinstance(i, list):
                make_dir(i)
                for _ in i:
                    self.assertTrue(os.path.isdir(_))
                    clean_dir(_)
                    self.assertFalse(os.path.isdir(_))
            else:
                make_dir(i)
                self.assertTrue(os.path.isdir(i))
                clean_dir(i)
                self.assertFalse(os.path.isdir(i))

        dir_list = ['/not_exists_dir_test_123']
        for i in dir_list:
            make_dir(i)
            self.assertFalse(os.path.isdir(i))

    def test_get_localhost_ip(self):
        ip = get_localhost_ip(domain='not_exists_domain')
        self.assertEqual(ip, "127.0.0.1")

        ip = get_localhost_ip()
        self.assertTrue(check_ip(ip_addr=ip))

    def test_get_total_page(self):
        self.assertEqual(get_total_page(total=880, page_size=30), 30)
        self.assertEqual(get_total_page(total='880 ', page_size=30), 30)
        with self.assertRaises(ValueError) as _:
            get_total_page(total='0x880', page_size=30)

    def test_get_dir_size(self):
        etc_size = get_dir_size('/etc')
        self.assertTrue(isinstance(etc_size, int))
        self.assertTrue(etc_size > 10)
        self.assertTrue(isinstance(get_dir_size('/not_exists_dir_test_123'), int))
        self.assertEqual(get_dir_size('/not_exists_dir_test_123'), 0)

    def test_str_to_list(self):
        self.assertTrue(isinstance(str_to_list('1,2,3.0'), list))
        self.assertTrue(isinstance(str_to_list('1'), list))
        self.assertTrue(isinstance(str_to_list(12313), list))
        self.assertTrue(isinstance(str_to_list([]), list))

    def test_get_risk_by_severity(self):
        self.assertEqual(get_risk_by_severity('Blocker'), 1)
        self.assertEqual(get_risk_by_severity('Critical'), 1)
        self.assertEqual(get_risk_by_severity('Major'), 2)
        self.assertEqual(get_risk_by_severity('Minor'), 3)
        self.assertEqual(get_risk_by_severity('not_found'), 4)

    def test_get_issue_type_by_sonar(self):
        self.assertEqual(get_issue_type_by_sonar('bug'), 1)
        self.assertEqual(get_issue_type_by_sonar('BUG'), 1)
        self.assertEqual(get_issue_type_by_sonar('code smell'), 2)
        self.assertEqual(get_issue_type_by_sonar('CODE_smell'), 2)
        self.assertEqual(get_issue_type_by_sonar('VULNERABILITY'), 3)

    def test_strip(self):
        self.assertEqual(strip(b' 1 '), b'1')
        self.assertEqual(strip("   "), '')
        self.assertEqual(strip(1), 1)
        self.assertEqual(strip([]), [])
        self.assertEqual(strip(" Admin ", "lower"), "admin")
        self.assertEqual(strip(" Admin ", "upper"), "ADMIN")

    def test_checkFile(self):
        f_p = os.path.join(BASEDIR, 'tests', 'data', 'tmp')
        f_f = os.path.join(f_p, 'test.txt')
        make_dir(f_p)
        with self.assertRaises(Exception) as _:
            checkFile("'not_found")
        with open(f_f, 'wb') as fp:
            fp.write(b'')
        self.assertTrue(checkFile(f_f))
        clean_dir(f_p)
