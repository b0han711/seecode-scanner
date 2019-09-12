# coding: utf-8

import os
import glob
import sys
import inspect
import gevent

from gevent.threadpool import ThreadPool

from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.common import get_git_author
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import hash_md5
from seecode_scanner.lib.core.common import find_text
from seecode_scanner.lib.engines import BaseScanner
from seecode_scanner.lib.engines.entity.plugin import Plugin
from seecode_scanner.lib.controller.vulnerability import Vulnerability
from seecode_scanner.lib.core.execptions import ScriptFileNotFound


class PluginScanner(BaseScanner):

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.component_rule = []
        self.whitelist_rule = []
        self.blacklist_rule = []
        self._key = 3

    def __plugin_format(self, node):
        """

        :param node:
        :return:
        """
        result = None
        if node:
            kwargs = {}
            node_id = node.get('id')
            kwargs['id'] = parse_int_or_str(node_id)
            risk_node = node.find("risk")
            kwargs['risk_id'] = parse_int_or_str(risk_node.get('id'))
            kwargs['risk_name'] = parse_int_or_str(risk_node.text)
            category_node = node.find("category")
            kwargs['category_id'] = parse_int_or_str(category_node.get('id'))
            kwargs['category_name'] = parse_int_or_str(category_node.text)

            kwargs['name'] = parse_int_or_str(find_text(node, "name"))
            kwargs['key'] = parse_int_or_str(find_text(node, "key"))
            kwargs['module'] = parse_int_or_str(find_text(node, "module"))
            kwargs['script'] = parse_int_or_str(find_text(node, "script"))

            script_path = os.path.join(paths.ROOT_PATH, kwargs['script'])
            if not os.path.isfile(script_path):
                raise ScriptFileNotFound("".format(script_path))

            dirname, filename = os.path.split(script_path)
            dirname = os.path.abspath(dirname)

            if filename.endswith('.pyc'):
                pluginName = filename[:-4]
            else:
                pluginName = filename[:-3]

            if dirname not in sys.path:
                sys.path.insert(0, dirname)
            try:
                if pluginName in sys.modules:
                    del sys.modules[pluginName]
                module = __import__(pluginName)
                _ = dict(inspect.getmembers(module))
                if "run" not in _:
                    self.log("[PluginScanner] missing function 'run(**kwargs)' in script '{0}'".format(script_path), 'error')
                else:
                    kwargs['func'] = _["run"]
                    result = Plugin(**kwargs)
            except ImportError as ex:
                self.log("[PluginScanner] cannot import script '{0}' ({1})".format(pluginName, ex), 'error')

        return result

    def load_component(self, items):
        """

        :param items:
        :return:
        """
        for item in items:
            plugin = self.__plugin_format(item)
            if plugin:
                self.component_rule.append(plugin)

    def load_blacklist(self, items):
        """

        :param items:
        :return:
        """
        for item in items:
            plugin = self.__plugin_format(item)
            if plugin:
                self.blacklist_rule.append(plugin)

    def load_whitelist(self, items):
        """

        :param items:
        :return:
        """
        for item in items:
            plugin = self.__plugin_format(item)
            if plugin:
                self.whitelist_rule.append(plugin)

    def start_component(self, project):
        pass

    def start_blacklist(self, project):
        """

        :param project:
        :return:
        """
        def __scan(file_path):
            for rule in self.blacklist_rule:
                flag = rule.verify(file_path)
                if flag:
                    rule.get_info(file_path)
                    if project.web_url:
                        report = '{0}/blob/{1}/{2}#L{3}'.format(
                            project.web_url,
                            project.branch,
                            file_path,
                            rule.start_line
                        )
                    else:
                        report = ''
                    author, author_email = get_git_author(project.get_last_author(file_path))
                    vuln = Vulnerability(
                        task_id=project.task_id,
                        rule_key=rule.key,
                        risk_id=rule.risk_id,
                        title=rule.name,
                        file=file_path,
                        author=author,
                        author_email=author_email,
                        hash=project.get_last_commit(),
                        start_line=rule.start_line,
                        end_line=rule.end_line,
                        report=report,
                        code_example=rule.code_example,
                        engine=self.key,
                    )
                    vuln_key = hash_md5('{0}_{1}_{2}'.format(file_path, rule.id, rule.start_line))
                    if vuln_key not in kb.result[project.key]:
                        kb.result[project.key][vuln_key] = vuln.info
                        project.logger.debug('[PluginScanner] {0}'.format(vuln))

        pool = ThreadPool(project.threads)
        for fpath, dirs, fs in os.walk(project.scan_path):
            for f in fs:
                pool.spawn(__scan,  os.path.join(fpath, f))
            gevent.wait()

    def start_whitelist(self, project):
        project.logger.info("[PluginScanner] False positive plugin processing...")
        pass
        project.logger.info("[PluginScanner] Plugin whitelist scan completed.")

