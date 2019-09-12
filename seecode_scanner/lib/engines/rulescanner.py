# coding: utf-8

import gevent
import os

from gevent.threadpool import ThreadPool

from seecode_scanner.lib.engines import BaseScanner
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import hash_md5
from seecode_scanner.lib.core.common import find_text
from seecode_scanner.lib.core.common import get_git_author
from seecode_scanner.lib.engines.entity.dir import DirRule
from seecode_scanner.lib.engines.entity.file import FileRule
from seecode_scanner.lib.engines.entity.content import ContentRule
from seecode_scanner.lib.engines.entity.component import ComponentRule
from seecode_scanner.lib.controller.vulnerability import Vulnerability
from seecode_scanner.lib.core.data import kb


class RuleScanner(BaseScanner):

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)

        self.component_rule = []
        self.whitelist_rule = []
        self.blacklist_rule = []
        self._key = 2

    def __rule_format(self, node):
        kwargs = {}
        if node:
            node_id = node.get('id')
            kwargs['id'] = parse_int_or_str(node_id)
            risk_node = node.find("risk")
            kwargs['risk_id'] = parse_int_or_str(risk_node.get('id'))
            kwargs['risk_name'] = parse_int_or_str(risk_node.text)
            category_node = node.find("category")
            kwargs['category_id'] = parse_int_or_str(category_node.get('id'))
            kwargs['category_name'] = parse_int_or_str(category_node.text)
            match_regex_node = node.find("match_regex")
            kwargs['regex_flag'] = parse_int_or_str(match_regex_node.get('flag'))
            kwargs['regex'] = parse_int_or_str(match_regex_node.text)

            kwargs['name'] = parse_int_or_str(find_text(node, "name"))
            kwargs['key'] = parse_int_or_str(find_text(node, "key"))
            kwargs['match_type'] = parse_int_or_str(find_text(node, "match_type"))
            kwargs['file_ext'] = parse_int_or_str(find_text(node, "match_ext"))
            kwargs['size'] = parse_int_or_str(find_text(node, "size"))
            kwargs['match_content'] = parse_int_or_str(find_text(node, "match_content"))

        return kwargs

    def load_component(self, items):
        """

        :param items:
            <item id="7582">
                <name>apache solr 远程代码执行</name>
                <key>apache:solr-rce-cve-2019-1123</key>
                <revision>0.08</revision>
                <risk id="2">高危</risk>
                <category>Vulnerability</category>
                <match_type>name</match_type>
                <match_content>fasjson</match_content>
                <match_regex flag="I">.*?</match_regex>
            </item>
        :return:
        """
        for item in items:
            kwargs = self.__rule_format(item)
            rule = ComponentRule(**kwargs)
            self.component_rule.append(rule)

    def load_blacklist(self, items):
        """

        :param items:
        :return:
        """
        for item in items:
            kwargs = self.__rule_format(item)

            if kwargs['match_type'] == 'dir':
                rule = DirRule(**kwargs)
                self.blacklist_rule.append(rule)
            elif kwargs['match_type'] == 'file':
                rule = FileRule(**kwargs)
                self.blacklist_rule.append(rule)
            elif kwargs['match_type'] == 'content':
                rule = ContentRule(**kwargs)
                self.blacklist_rule.append(rule)

    def load_whitelist(self, items):
        for item in items:
            kwargs = self.__rule_format(item)

            if kwargs['match_type'] == 'dir':
                rule = DirRule(**kwargs)
                self.whitelist_rule.append(rule)
            elif kwargs['match_type'] == 'file':
                rule = FileRule(**kwargs)
                self.whitelist_rule.append(rule)
            elif kwargs['match_type'] == 'content':
                rule = ContentRule(**kwargs)
                self.whitelist_rule.append(rule)

    def start_component(self, project):
        """

        :param project:
        :return:
        """

        project.logger.info("[RuleScanner] Begin to perform rule-based component vulnerability analysis...")
        same_result = []
        for rule in self.component_rule:
            project.logger.debug("[RuleScanner] Test '{0}' rule...".format(rule.name))
            for component in project.statistics['depends']:
                flag, _ = rule.verify(
                    component_name=component['name'],
                    version=component['version'],
                    group_id=component['tag']
                )
                msg = "[RuleScanner] group_id: [{0}], component name: [{1}], component version: [{2}], status: [{3}], " \
                      "result: [{4}]".format(component['tag'], component['name'], component['version'], flag, _)
                project.logger.debug(msg)

                if flag:
                    origin_file = component['origin']
                    # include find vuln
                    if component['parent_origin'] and project.component_same_vuln_merge_enable:
                        key = '{0}_{1}'.format(rule.key, component['parent_origin'])
                        if key in same_result:
                            continue
                        else:
                            origin_file = component['parent_origin']
                            same_result.append(key)
                    else:  # origin find vuln
                        key = '{0}_{1}'.format(rule.key, component['origin'])
                        same_result.append(key)
                    project.logger.info("[RuleScanner] [Component] [+] Found '{0}' vulnerability.".format(rule.name))
                    info = rule.get_info(
                        match_content=_,
                        origin_file=os.path.join(project.scan_path, component['origin']),
                        evidence_start_line_offset=project.evidence_start_line_offset,
                        evidence_count=project.evidence_count
                    )
                    if project.web_url:
                        report = '{0}/blob/{1}/{2}#L{3}'.format(
                            project.web_url,
                            project.branch,
                            origin_file,
                            info['start_line']
                        )
                    else:
                        report = ''
                    author, author_email = get_git_author(project.get_last_author(component['origin']))
                    vuln = Vulnerability(
                        task_id=project.task_id,
                        rule_key=rule.key,
                        risk_id=rule.risk_id,
                        title=rule.name,
                        file=origin_file,
                        author=author,
                        author_email=author_email,
                        hash=project.get_last_commit(),
                        start_line=info['start_line'],
                        end_line=info['end_line'],
                        report=report,
                        code_example=info['code_example'],
                        evidence_content=_,
                        engine=self.key,
                    )
                    vuln_key = hash_md5('{0}_{1}_{2}'.format(component['origin'], rule.id, info['start_line']))
                    if vuln_key not in kb.result[project.key]:
                        kb.result[project.key][vuln_key] = vuln.info
                        project.logger.debug('[RuleScanner] {0}'.format(vuln))

        project.logger.info("[RuleScanner] Rule component scan completed.")

    def start_blacklist(self, project):
        """

        :param project:
        :return:
        """
        def __scan(file_path):
            for rule in self.blacklist_rule:
                flag, _ = rule.verify(reference_value=file_path)
                project.logger.debug("[RuleScanner] rule: [{0}], file: [{1}]".format(rule, file_path))
                if flag:
                    relative_path = file_path.replace(project.scan_path, "")
                    project.logger.info("[RuleScanner] [Blacklist] [+] Found '{0}' vulnerability in '{1}' file.".format(rule.name, relative_path))
                    info = rule.get_info(match_content=_, origin_file=file_path)
                    if project.web_url:
                        report = '{0}/blob/{1}{2}#L{3}'.format(
                            project.web_url,
                            project.branch,
                            relative_path,
                            info['start_line']
                        )
                    else:
                        report = ''
                    author, author_email = get_git_author(project.get_last_author(file_path))
                    vuln = Vulnerability(
                        task_id=project.task_id,
                        rule_key=rule.key,
                        risk_id=rule.risk_id,
                        title=rule.name,
                        file=relative_path,
                        author=author,
                        author_email=author_email,
                        hash=project.get_last_commit(),
                        start_line=info['start_line'],
                        end_line=info['end_line'],
                        report=report,
                        code_example=info['code_example'],
                        evidence_content=_,
                        engine=self.key,
                    )
                    vuln_key = hash_md5('{0}_{1}_{2}'.format(file_path, rule.id, info['start_line']))
                    if vuln_key not in kb.result[project.key]:
                        kb.result[project.key][vuln_key] = vuln.info
                        project.logger.debug('[RuleScanner] {0}'.format(vuln))

        project.logger.info("[RuleScanner] Begin to perform rule-based blacklist vulnerability analysis...")
        pool = ThreadPool(project.threads or 20)
        for fpath, dirs, fs in os.walk(project.scan_path):
            for f in fs:
                pool.spawn(__scan,  os.path.join(fpath, f))
            gevent.wait()

        project.logger.info("[RuleScanner] Rule blacklist scan completed.")

    def start_whitelist(self, project):
        """

        :param project:
        :return:
        """
        project.logger.info("[RuleScanner] False positive rule processing...")
        for k, v in kb.result[project.key].items():
            for rule in self.whitelist_rule:
                file_name, file_ext = os.path.splitext(v['file'])
                if rule.file_ext and file_ext.lower() not in rule.file_ext:
                    msg = "The file type can only be {0}, the current type: [{1}].".format(rule.file_ext, file_ext)
                    project.logger.warning("[RuleScanner] [Whitelist] [SKIP] {0}".format(msg))
                    continue
                project.logger.debug("[RuleScanner] Test '{0}' rule...".format(rule.name))
                flag, _ = rule.verify_result(content=v['code_example'])
                if flag:
                    project.logger.info(
                        "[RuleScanner] [Whitelist] [+] Found [{0}] as false positive, "
                        "verification rule: [{1}], "
                        "match content: [{2}].".format(v['file'], rule.name, _))
                    v['is_false_positive'] = True
                    v['whitelist_rule_id'] = rule.id
                    v['evidence_content'] = _

        project.logger.info("[RuleScanner] Rule whitelist scan completed.")
