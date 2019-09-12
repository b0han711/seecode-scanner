# coding: utf-8

import os

from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.engines.entity import BaseRule
from seecode_scanner.lib.core.execptions import FileLimitSizeException
from seecode_scanner.lib.core.execptions import FileLimitSuffixException


class ContentRule(BaseRule):

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
            file_name, file_ext = os.path.splitext(reference_value)

            if self._file_ext and file_ext.lower() not in self._file_ext:
                msg = "The file type can only be {0}, the current type: [{1}].".format(self._file_ext, file_ext)
                raise FileLimitSuffixException(msg)

            file_size = round(os.path.getsize(reference_value), 2)  # Bytes
            if self._file_size != 0 and file_size > self._file_size:
                msg = "[SKIP] file: {0}, size: {1}KB, limit size: {2}KB".format(
                    reference_value,
                    file_size,
                    self._file_size
                )
                raise FileLimitSizeException(msg)

            with open(reference_value, "rb") as fp:
                s = fp.read()
                if isinstance(s, bytes):
                    try:
                        content = s.decode('utf-8')
                    except:  # There will be problems with the binary
                        content = str(s)
                else:
                    content = s
                for r in self._regex:
                    _result = r.search(content)
                    if _result:
                        result = _result.group(0)
                        status = True
                        break

        return status, result
