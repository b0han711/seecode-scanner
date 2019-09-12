# coding: utf-8

import os
import gevent

from gevent.threadpool import ThreadPool
from func_timeout import func_timeout
from func_timeout import FunctionTimedOut

from seecode_scanner.lib.engines import BaseScanner
from seecode_scanner.lib.utils.command import GrepCMD
from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.common import get_line_content
from seecode_scanner.lib.core.common import hash_md5
from seecode_scanner.lib.core.common import get_risk_by_severity
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.core.common import get_git_author
from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.execptions import CodeBaseException
from seecode_scanner.lib.core.execptions import ScanFailedException
from seecode_scanner.lib.core.execptions import SonarScannerFailureException
from seecode_scanner.lib.core.execptions import EngineExecutionTimeoutException
from seecode_scanner.lib.core.settings import SONAR_PROJECT_PROPERTIES
from seecode_scanner.lib.controller.vulnerability import Vulnerability
from seecode_scanner.lib.utils.api_sonarqube import SonarAPIHandler


class SonarScanner(BaseScanner):

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.component_rule = {}
        self.whitelist_rule = {}
        self.blacklist_rule = {}
        self._grep = GrepCMD()
        self._key = 1
        self.sonarqube = None
        self.pool = ThreadPool(20)

    def load_component(self, items):
        pass

    def load_blacklist(self, items):
        pass

    def load_whitelist(self, items):
        pass

    def start_component(self, project):
        pass

    def start_whitelist(self, project):
        pass

    def start_blacklist(self, project):
        """

        :param project:
        :return:
        """
        project.logger.info("[SonarScanner] Start the start_blacklist method...")
        try:
            func_timeout(self._engine_timeout, self.__start_blacklist, args=(project,))
        except FunctionTimedOut as te:
            self.__kill_sonar_scanner_pid(project)
            msg = '[SonarScanner] sonar-scanner execution timeout, default timeout: {0}s.'.format(self._engine_timeout)
            project.update_scan_message(title='扫描超时', reason=msg, level=2)
            raise EngineExecutionTimeoutException(msg)
        project.logger.info("[SonarScanner] Sonar blacklist scan completed.")

    def __start_blacklist(self, project):
        """

        :param project:
        :return:
        """
        try:
            if not os.path.isfile(self._sonar_scanner_path):
                msg = "File path for 'sonar_scanner' not found, sonar_scanner_path: {0}".format(
                    self._sonar_scanner_path)
                raise SonarScannerFailureException(msg)

            self.sonarqube = SonarAPIHandler(
                token=self._api_token,
                logger=project.logger,
                sonar_server=self._api_domain,
                http_timeout_retry=self._http_timeout_retry,
                http_failed_retry=self._http_failed_retry,
                http_timeout=self._http_timeout,
            )

            self.__make_sonar_config(project)
            # 开始执行 sonar-scanner 命令
            exec_cmd(' '.join(
                ['cd', project.scan_path, '&&', self._sonar_scanner_path, '1>>{0} 2>&1 &'.format(project.log_file)]))
            if self._grep.exec_match(
                    cmd='"EXECUTION SUCCESS" {0}'.format(project.log_file),
                    match_str='EXECUTION SUCCESS'):
                self.__sync_issues(project)
            else:
                reason = self.__get_failed_reason(project)
                project.update_scan_message(title='EXECUTION FAILURE!', reason=reason, level=2)
                raise SonarScannerFailureException('[SonarScanner] EXECUTION FAILURE! {0}'.format(reason))
        except (CodeBaseException, gevent.exceptions.LoopExit) as ex:
            project.logger.error(ex)
            raise ex

    def __kill_sonar_scanner_pid(self, project):
        """

        :param project:
        :return:
        """
        try:
            project.logger.info('[SonarScanner] Get the pid number of the sonar-scanner ...')
            get_sonar_scanner_cmd = 'ps -ef | grep "cd ' + project.scan_path + ' \&\& ' + self._sonar_scanner_path + '"|grep -v grep|awk \'{print($2)}\''
            project.logger.debug('[SonarScanner] Query pid command: [{0}]'.format(get_sonar_scanner_cmd))
            pid, _ = exec_cmd(get_sonar_scanner_cmd)
            pid = parse_int_or_str(pid) or ''
            project.logger.debug('[SonarScanner] Get PID: [{0}]'.format(pid))
            if pid:
                sub_pid_cmd = 'ps -ef | grep "Dproject.home=' + project.scan_path + '"|grep -v grep|awk \'{print($2)}\''
                sub_pid, _ = exec_cmd(sub_pid_cmd)
                sub_pid = strip(sub_pid)
                if '\n' in sub_pid.decode("utf-8"):
                    sub_pid = [parse_int_or_str(_p) for _p in sub_pid.decode("utf-8").split("\n") if _p]
                else:
                    sub_pid = parse_int_or_str(sub_pid) or ''
                kill_sonar_scanner_cmd = 'kill -9 {0} {1}'.format(pid, sub_pid)
                status, _ = exec_cmd(kill_sonar_scanner_cmd)
                if _:
                    project.logger.warning('[SonarScanner] The termination of the sonar-scanner '
                                           'process failed with the command: [{0}]'.format(kill_sonar_scanner_cmd))
                else:
                    project.logger.info('[SonarScanner] Process [{0},{1}] is terminated.'.format(pid, sub_pid))
        except:
            pass

    def __get_failed_reason(self, project):
        """

        :return:
        """
        reason_msg = ''
        failed_msg = [
            'Failed to upload report',
            'SonarQube analysis without pushing the results to the SonarQube server.',
        ]
        for i in failed_msg:
            if self._grep.exec_match(cmd='"{0}" {1}'.format(i, project.log_file), match_str=i):
                return ScanFailedException('SonarQube 上传分析报告失败，请联系 SonarQube 管理员。')

        return reason_msg

    def __make_sonar_config(self, project):
        """

        :param project:
        :return:
        """
        sonar_conf_path = os.path.join(project.scan_path, 'sonar-project.properties')
        if not os.path.isfile(sonar_conf_path):
            scan_config = self._sonar_project_properties or SONAR_PROJECT_PROPERTIES
            scan_config = scan_config.replace('{{project_key}}', project.key)
            scan_config = scan_config.replace('{{project_name}}', project.name)
            scan_config = scan_config.replace('{{sonar_host}}', '{0}'.format(self._api_domain))
            scan_config = scan_config.replace('{{sonar_login}}', self._api_token)
            with open(sonar_conf_path, 'w') as fp:
                fp.write(scan_config)
            msg = "[SonarScanner] Didn't find the 'sonar-project.properties' file, " \
                  "create [{0}] using the default template.".format(sonar_conf_path)
            project.logger.warning(msg)
            project.update_scan_message(title="[SonarScanner] 没有找到 'sonar-project.properties'文件", reason=msg, level=3)

    def __sync_issues(self, project):
        """
        同步 sonar 的 issue
        :return:
        """

        project.logger.info('[SonarScanner] Start sync sonar issues...')
        try:
            for issue_list in self.sonarqube.get_issues(project_key=project.key):
                for issue in issue_list:
                    self.__create_issue(project, issue)
                    # self.pool.spawn(self.__create_issue, project, issue)  #
                # gevent.wait()
        except Exception as ex:
            project.logger.error(ex)

    def __create_issue(self, project, issue):
        """

        :param project:
        :param issue:
        :return:
        """
        try:
            if not issue and not isinstance(issue, dict):
                return
            start_line, end_line = 1, 1
            if 'textRange' in issue and ('startLine' in issue['textRange'] or 'endLine' in issue['textRange']):
                start_line = issue['textRange']['startLine']
                end_line = issue['textRange']['endLine']
            _, filename = issue['component'].split(':')
            author, author_email = get_git_author(project.get_last_author(filename))
            report_detail_url = '{0}component?id={1}&line={2}'.format(self._api_domain, issue['component'], start_line)
            code_segment = get_line_content(
                file=os.path.join(project.scan_path, filename),
                start_line=start_line + int(project.evidence_start_line_offset),
                count=project.evidence_count
            )
            vuln = Vulnerability(
                task_id=project.task_id,
                risk_id=get_risk_by_severity(issue['severity']),
                rule_key=issue['rule'],
                category=issue['type'],
                title=issue['message'],
                file=filename,
                author=author,
                author_email=author_email,
                hash=project.get_last_commit(),
                start_line=start_line,
                end_line=end_line,
                report=report_detail_url,
                code_example=''.join(code_segment),
                engine=self.key,
            )

            vuln_key = hash_md5('{0}_{1}_{2}'.format(filename, issue['rule'], start_line))

            if vuln_key not in kb.result[project.key]:
                kb.result[project.key][vuln_key] = vuln.info

        except Exception as ex:
            import traceback;traceback.print_exc()
            project.logger.error(ex)
