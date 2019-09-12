# coding: utf-8

from __future__ import absolute_import

import os
import sys
import unittest

BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(BASEDIR)


class TestCase(unittest.TestCase):
    """

    """

    skipTest = True

    def setUp(self):
        pass

    def tearDown(self):
        pass
