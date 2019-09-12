# coding: utf-8

import json
import os


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class DumpReport(object):

    def __init__(self, save_path):
        self.save_path = save_path

    def save(self, result):

        with open(self.save_path, 'w', encoding="utf-8") as fp:
            json.dump(result, fp, cls=JsonEncoder, indent=4)
