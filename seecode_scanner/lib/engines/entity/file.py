# coding: utf-8

import os

from seecode_scanner.lib.engines.entity import BaseRule
from seecode_scanner.lib.core.common import strip


class FileRule(BaseRule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def verify(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        reference_value = strip(kwargs.get('reference_value'))

        status, result = False, ''
        if os.path.isfile(reference_value):
            for r in self._regex:
                _result = r.search(reference_value)
                if _result:
                    result = _result.group(0)
                    status = True
                    break
        return status, result

