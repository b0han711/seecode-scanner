# coding: utf-8

import os
from inspect import isfunction

from seecode_scanner.lib.engines.entity import BaseRule
from seecode_scanner.lib.core.common import strip


class Plugin(BaseRule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def verify(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        reference_value = strip(kwargs.get('file'))
        status, result = False, ''
        if os.path.isfile(reference_value) and isfunction(self._func):
            status, result = self._func(file=reference_value)
        return status, result

    def verify_result(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        vuln = strip(kwargs.get('vuln'))

        status, result = self._func(
            code_path=vuln.project_scan_path,
            title=vuln.title,
            file_name=vuln.file,
            start_line=vuln.start_line,
            end_line=vuln.end_line,
            file_content=vuln.code_example,
        )
        return status, result
