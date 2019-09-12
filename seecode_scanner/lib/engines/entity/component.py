# coding: utf-8

from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.engines.entity import BaseRule


class ComponentRule(BaseRule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def verify(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        component_name = strip(kwargs.get('component_name'))
        version = strip(kwargs.get('version'))
        group_id = strip(kwargs.get('group_id'), None)
        status, result = False, ''

        if self._match_type and self._match_type.lower() != 'name':
            if self._match_content == group_id:
                for r in self._regex:
                    _result = r.search(version)
                    if _result:
                        result = _result.group(0)
                        status = True
                        break
        else:
            if component_name and self._match_content == component_name:
                for r in self._regex:
                    _result = r.search(version)
                    if _result:
                        result = _result.group(0)
                        status = True
                        break
        return status, result
