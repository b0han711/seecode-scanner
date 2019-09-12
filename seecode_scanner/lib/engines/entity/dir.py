# coding: utf-8
import os

from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.engines.entity import BaseRule


class DirRule(BaseRule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def verify(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        reference_value = strip(kwargs.get("reference_value"))
        scan_path = strip(kwargs.get("scan_path"))

        status, result = False, ''
        if os.path.isfile(reference_value):
            reference_value = '{0}/'.format(os.path.dirname(reference_value))

        if os.path.isdir(reference_value):
            if scan_path:
                work_dir = reference_value.replace(scan_path, '')
            else:
                work_dir = reference_value
            for r in self._regex:
                _result = r.search(work_dir)
                if _result:
                    result = _result.group(0)
                    status = True
                    break
        return status, result
