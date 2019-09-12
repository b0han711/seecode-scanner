# coding: utf-8

import re
import os

from seecode_scanner.lib.core.common import get_line_content
from seecode_scanner.lib.core.common import get_str_line
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.common import strip


class BaseRule(object):

    def __init__(self, **kwargs):
        self._id = parse_int(kwargs.get('id'))
        self._name = strip(kwargs.get('name'), None)
        self._description = strip(kwargs.get('description'), '')
        self._key = strip(kwargs.get('key'), 'lower')
        self._risk_id = parse_int(kwargs.get('risk_id'))
        self._risk_name = strip(kwargs.get('risk_name'))
        self._category_id = parse_int(kwargs.get('category_id'))
        self._category_name = strip(kwargs.get('category_name'), None)
        regex = strip(kwargs.get('regex'), None)
        regex_flag = strip(kwargs.get('regex_flag'), None)

        self._file_ext = strip(kwargs.get('file_ext'), None)  # File extension
        self._file_size = parse_int(kwargs.get('size'), 0)  # File size

        self._match_type = strip(kwargs.get('match_type'), None)  # match type: groupId、name
        self._match_ext = strip(kwargs.get('match_ext'), None)  # match type: groupId、name
        self._match_content = strip(kwargs.get('match_content'), None)  # match content
        self._func = kwargs.get('func')

        if self._file_ext:
            file_ext = []
            self._file_ext = self._file_ext.split(',')
            for item in self._file_ext:
                ext = item.lower().strip()
                file_ext.append(ext[ext.find("."):])
            self._file_ext = file_ext

        self._flag = None
        self._regex = []

        if regex_flag and 'I' in regex_flag and 'M' in regex_flag:
            self._flag = re.I | re.M
        elif regex_flag and 'M' in regex_flag:
            self._flag = re.M
        elif regex_flag and 'I' in regex_flag:
            self._flag = re.I

        if regex:
            for r in regex.split("\n"):
                if " ###" in r:
                    expr = r[:r.find(" ###")]
                    expr = expr.strip()
                else:
                    expr = r.strip()
                if self._flag:
                    self._regex.append(re.compile(expr, self._flag))
                else:
                    self._regex.append(re.compile(expr))

    def __str__(self):
        metadata = {
            'id': self._id,
            'name': self._name,
            'description': self._description,
            'key': self._key,
            'risk_id': self._risk_id,
            'risk_name': self._risk_name,
            'category_id': self._category_id,
            'category_name': self._category_name,
            'file_ext': self._file_ext,
            'file_size': self._file_size,
            'match_type': self._match_type,
            'match_content': self._match_content,
            'regex': self._regex,
            'regex_flag': self._flag,
        }
        return str(metadata)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def risk(self):
        return self._risk_name

    @property
    def risk_id(self):
        return self._risk_id

    @property
    def key(self):
        return self._key

    @property
    def file_ext(self):
        return self._file_ext

    @property
    def category(self):
        return self._category_name

    def verify(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        raise NotImplemented()

    def verify_result(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        content = strip(kwargs.get('content'))
        status, result = False, ''

        if isinstance(content, bytes):
            try:
                content = content.decode('utf-8')
            except:  # There will be problems with the binary
                content = str(content)

        for r in self._regex:
            _result = r.search(content)
            if _result:
                result = _result.group(0)
                status = True
                break

        return status, result

    def get_info(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        origin_file = strip(kwargs.get('origin_file'))
        match_content = strip(kwargs.get('match_content'))
        evidence_start_line_offset = parse_int(kwargs.get('evidence_start_line_offset'), -1)
        evidence_count = parse_int(kwargs.get('evidence_count'), 5)

        result = {
            'start_line': 0,
            'end_line': 0,
            'code_example': '',
        }

        if os.path.isfile(origin_file) and match_content:
            contents = []
            with open(origin_file, 'rb') as fp:
                contents = fp.readlines()
                result['start_line'] = get_str_line(match_content, contents)

            if result['start_line'] > 0:
                result['end_line'] = result['start_line'] + 1
                result['code_example'] = get_line_content(
                    file=contents,
                    start_line=result['start_line'] + int(evidence_start_line_offset),
                    count=int(evidence_count))
                if result['code_example']:
                    result['code_example'] = ''.join(result['code_example'])
        return result
