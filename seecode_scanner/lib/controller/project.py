# encoding: utf-8

import datetime
import logging
import os
import sys
import gc

from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

from seecode_scanner.lib.controller.task import TaskStatus
from seecode_scanner.lib.core.common import clean_dir
from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.common import get_dir_size
from seecode_scanner.lib.core.common import get_project_scope
from seecode_scanner.lib.core.common import make_dir
from seecode_scanner.lib.core.common import parse_bool
from seecode_scanner.lib.core.common import parse_int
from seecode_scanner.lib.core.common import parse_int_or_str
from seecode_scanner.lib.core.common import strip
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import paths
from seecode_scanner.lib.core.dump import DumpReport
from seecode_scanner.lib.core.execptions import DistributedConfigurationInvalid
from seecode_scanner.lib.core.execptions import DistributedDoesNotSupportStorage
from seecode_scanner.lib.core.execptions import MissingImportantScanParameters
from seecode_scanner.lib.core.execptions import ScanDirectoryIsEmpty
from seecode_scanner.lib.core.execptions import ScanTemplateNotFound
from seecode_scanner.lib.core.option import init
from seecode_scanner.lib.core.option import load_scan_template
from seecode_scanner.lib.utils.command import CopyCMD
from seecode_scanner.lib.utils.command import FindCMD
from seecode_scanner.lib.utils.ftpwrapper import FTPWork
from seecode_scanner.lib.utils.gitwrapper import GitOperator

try:
    from clocwalk import ClocDetector
    from clocwalk.lib.exception import CodeDirIsNoneException
except ImportError as ex:
    logger.warning("[ScanProject] python clocwalk is not installed.")


class ScanProject(object):

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self._logger = None
        self._paths_log = ''
        self._log_file = ''
        self._remote_paths = ''
        self._paths_project_origin = None
        self._paths_project_scan = None
        self._branch_commit = None
        self._git = None
        self._rotate_handler = None
        self._statistics = {
            'depends': [],
            'file': [],
            'total': 0,
            'size': 0,  # KB
            'language': '',
            'risk': {},
        }

        # scan
        self._threads = parse_int_or_str(parse_int(kwargs.get('threads'), 20))
        self._template = strip(kwargs.get('template'), display_type='lower')
        self._template_full_path = strip(kwargs.get('template_full_path'))
        self._work_dir = kwargs.get('work_dir') or '/data/seecode'
        self._log_level = strip(kwargs.get('log_level')) or 'info'
        self._task_id = parse_int(kwargs.get('task_id'))
        self._project_name = strip(kwargs.get('project_name'))
        self._project_branch = strip(kwargs.get('project_branch'))
        self._project_ssh = strip(kwargs.get('project_ssh'))
        self._project_web = strip(kwargs.get('project_web'))
        self._project_local_path = strip(kwargs.get('project_local_path'))
        self._project_type = strip(kwargs.get('project_type') or 'offline', display_type='lower')
        self._project_storage_type = strip(kwargs.get('project_storage_type'), display_type='lower')
        self._project_file_origin_name = strip(kwargs.get('project_file_origin_name'))
        self._project_file_hash = strip(kwargs.get('project_file_hash'))
        self._group_name = strip(kwargs.get('group_name'))
        self._group_key = strip(kwargs.get('group_key'))
        # 强制更新代码，必须为线上项目
        self._force_sync_code = parse_bool(kwargs.get('force_sync_code', False))
        # 强制扫描项目
        self._force_project_scan = parse_bool(kwargs.get('force_project_scan', False))
        # 同步漏洞到 SeeCode Audit 服务端
        self._sync_vuln_to_server = parse_bool(kwargs.get('sync_vuln_to_server', False))
        # 取证偏移
        self._evidence_start_line_offset = parse_int(kwargs.get('evidence_start_line_offset'), -1)
        # 合并相同组件漏洞（依赖文件包含）
        self._component_same_vuln_merge_enable = parse_bool(kwargs.get('component_same_vuln_merge_enable', True))

        self._evidence_count = parse_int(kwargs.get('evidence_count'), 5)
        self._result_file = strip(kwargs.get('result_file'))
        self._result_format = strip(kwargs.get('result_format'))
        self._is_cli_call = parse_bool(kwargs.get('is_cli_call'))
        self._issue_statistic_type = ['vulnerability']
        self._send_size = parse_int_or_str(strip(kwargs.get('send_size', 50)))

        # distributed
        self._distributed = kwargs.get('distributed', conf.distributed)
        self.storage = {}

        self.__check_scan_parameters()
        self.__init_work_dir()
        self.__init_logger()
        self.cp = CopyCMD()
        self.find = FindCMD()

        # check scan template
        profile = os.path.join(paths.ROOT_PROFILE_PATH, '{0}.xml'.format(self._template))
        stat = os.stat(profile)
        if not all((kb, kb.profiles)):
            init()
            if self._template_full_path and os.path.isfile(self._template_full_path):
                load_scan_template(template_file_path=self._template_full_path)
            else:
                load_scan_template()

            kb.profiles_time[self._template] = stat.st_ctime

        if kb.profiles_time[self._template] != stat.st_ctime:
            load_scan_template()
            kb.profiles_time[self._template] = stat.st_ctime

        # result
        if self.key not in kb.result:
            kb.result[self.key] = {}

        if not self._result_file:
            self._result_file = '{0}.json'.format(self._task_id or self._project_name)
        if not self._result_file.startswith('/'):
            self._result_file = os.path.join(self._paths_log, self._result_file)

        # remote storage
        self.__init_distributed()
        self._remote_log = os.path.join(self._remote_paths, os.path.basename(self._log_file))
        self._remote_result = os.path.join(self._remote_paths, os.path.basename(self._result_file))

        # scan task
        if isinstance(self._task_id, int):
            self._task_status = TaskStatus(
                task_id=self._task_id,
                server=conf.server.domain,
                server_token=conf.server.token,
                logger=self.logger
            )
            if self._sync_vuln_to_server:
                self._task_status.update_initialization(
                    scan_template=self._template,
                    scan_template_version=kb.profiles[self._template].version,
                    log_path=self._remote_log,
                )
        else:
            self._task_status = None

        if self._template not in kb.profiles:
            msg = "[ScanProject] Didn't find '{0}' template.".format(self._template)
            if self._task_status and self._sync_vuln_to_server:
                self.update_scan_failed_status(msg)
            raise ScanTemplateNotFound(msg)

    def __del__(self):
        if self.key in kb.result:
            del kb.result[self.key]
        gc.collect()

    @property
    def task_id(self):
        return self._task_id

    @property
    def task(self):
        return self._task_status

    @property
    def threads(self):
        return self._threads

    @property
    def name(self):
        return self._project_name

    @property
    def key(self):
        return '{0}_{1}'.format(self._project_name, self._project_branch)

    @property
    def template_name(self):
        return self._template

    @property
    def log_file(self):
        return self._log_file

    @property
    def branch(self):
        return self._project_branch

    @property
    def branch_commit(self):
        return self._branch_commit

    @property
    def type(self):
        return self._project_type

    @property
    def statistics(self):
        return self._statistics

    @property
    def send_size(self):
        return self._send_size

    @property
    def logger(self):
        return self._logger

    @property
    def log_level(self):
        if self._log_level == "debug":
            return logging.DEBUG
        elif self._logger == "error":
            return logging.ERROR
        elif self._logger == "warn":
            return logging.WARN
        else:
            return logging.INFO

    @property
    def origin_path(self):
        return self._paths_project_origin

    @property
    def scan_path(self):
        return self._paths_project_scan

    @property
    def task_status(self):
        return self._task_status

    @property
    def web_url(self):
        return self._project_web

    @property
    def evidence_start_line_offset(self):
        return self._evidence_start_line_offset

    @property
    def evidence_count(self):
        return self._evidence_count

    @property
    def sync_vuln_to_server(self):
        return self._sync_vuln_to_server

    @property
    def component_same_vuln_merge_enable(self):
        return self._component_same_vuln_merge_enable

    def get_last_author(self, file):
        """

        :param file:
        :return:
        """
        author = ''
        if self._git:
            author = self._git.get_commit_author(file)
        return author

    def get_last_commit(self):
        """

        :return:
        """
        if self._git:
            if not self._branch_commit:
                self._branch_commit = self._git.get_branch_last_commit_id()
            return self._branch_commit
        else:
            return ''

    def __check_scan_parameters(self):
        """

        :return:
        """
        if self._project_type == 'online':
            if not all((self._project_name, self._project_branch, self._project_ssh,
                        self._group_key, self._template, self._work_dir)):
                msg = "[ScanProject] Missing 'project_name, project_branch, project_ssh, group_key, template, " \
                      "work_dir' important scan parameters."
                raise MissingImportantScanParameters(msg)
        elif self._project_local_path:
            if not os.path.isdir(self._project_local_path):
                raise IOError('"{0}" is not found.'.format(self._project_local_path))
        else:
            if not all((self._project_name, self._project_storage_type, self._template, self._work_dir)):
                msg = "[ScanProject] Missing 'project_name, project_storage_type, template, " \
                      "work_dir' important scan parameters."
                raise MissingImportantScanParameters(msg)

    def __init_distributed(self):
        """

        :return:
        """
        debug = False
        if self._distributed:
            try:
                if self._log_level == "debug":
                    debug = True
                if 'ftp' == self._project_storage_type.lower().strip():
                    try:
                        self.storage['ftp'] = FTPWork(
                            host=self._distributed['ftp']['host'],
                            port=parse_int(self._distributed['ftp']['port'], 21),
                            username=self._distributed['ftp']['username'],
                            password=self._distributed['ftp']['password'],
                            debug=debug,
                        )
                        self._remote_paths = os.path.join(
                            self._distributed['ftp']['path'],
                            'tasks',
                            '{0}'.format(self._task_id or self._project_name)
                        )
                        self.storage[self._project_storage_type].make_dir(self._remote_paths)
                        self._logger.info('Start creating ftp upload directory: {0}.'.format(self._remote_paths))
                    except Exception as ex:
                        msg = "[ScanProject] Failed to connect to the FTP service. " \
                              "Please check if the service is available."
                        raise Exception(msg)
                elif 'aws' == self._project_storage_type.lower().strip():
                    self.storage['aws'] = {}
                    pass  # TODO
                elif 'local' == self._project_storage_type.lower().strip():
                    pass
                else:
                    msg = 'Does not support "{0}" storage mode.'.format(self._project_storage_type)
                    self._logger.warning(msg)

            except Exception as ex:
                import traceback;
                traceback.print_exc()
                msg = "[ScanProject] The distributed parameter configuration may have an error and " \
                      "cannot connect to the service. {0}".format(str(ex))
                raise DistributedConfigurationInvalid(msg)
        elif self._project_local_path:  # local scan
            pass
        else:
            msg = "[ScanProject] Missing 'distributed' important scan parameters."
            raise MissingImportantScanParameters(msg)

    def __init_work_dir(self):
        """

        :return:
        """
        scan_work = '{0}'.format(self._task_id or self._project_name)
        self._paths_log = os.path.join(self._work_dir, 'logs', scan_work)
        self._paths_project_origin = os.path.join(self._work_dir, 'projects', self._group_key or self._project_name)
        self._project_path = os.path.join(self._paths_project_origin, self._project_name)
        self._paths_project_scan = os.path.join(self._work_dir, 'tasks', scan_work)

        if os.path.isdir(self._paths_project_scan):
            clean_dir(self._paths_project_scan)
        make_dir([self._paths_log, self._paths_project_origin, self._paths_project_scan])

    def __init_logger(self):
        """

        :return:
        """
        if self._task_id:
            log_name = '{0}.log'.format(self._task_id)
        else:
            log_name = '{0}.log'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

        self._log_file = os.path.join(self._paths_log, log_name)
        self._logger = logging.getLogger("seecode-scanner")
        self._rotate_handler = RotatingFileHandler(self._log_file, "w", 100 * 1024 * 1024, 1, encoding='utf-8')  # 100mb
        if self._log_level == "debug":
            formatter = logging.Formatter(
                "[%(asctime)s] [%(pathname)s(%(lineno)d)%(funcName)s()] [%(levelname)s] %(message)s", "%H:%M:%S")
        else:
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
        self._rotate_handler.setFormatter(formatter)
        try:
            from seecode_scanner.lib.core.ansistrm import ColorizingStreamHandler
            logger_handler = ColorizingStreamHandler(sys.stdout)
        except ImportError:
            logger_handler = logging.StreamHandler(sys.stdout)

        if self._is_cli_call:
            logger_handler.setFormatter(formatter)
            self._logger.addHandler(logger_handler)
        self._logger.addHandler(self._rotate_handler)
        self._logger.setLevel(self.log_level)
        if self._project_type == 'online':
            self._git = GitOperator(
                project_path=self._project_path,
                git_url=self._project_ssh,
                logger=self._logger
            )

    def upload_result_log(self):
        """
        上传扫描结果与扫描日志
        :return:
        """
        if self._project_storage_type:
            try:
                self.__init_distributed()
                if self._project_storage_type == 'ftp':
                    self._logger.info('Upload the "{0}" file to ftp.'.format(self._remote_log))
                    self.storage[self._project_storage_type].upload_file(self._log_file, self._remote_log)
                    if self._result_file:
                        self._logger.info('Upload the "{0}" file to ftp.'.format(self._remote_result))
                        self.storage[self._project_storage_type].upload_file(self._result_file, self._remote_result)
                    self.storage[self._project_storage_type].close()
                # aws
                elif self._project_storage_type == 'aws':
                    raise Exception()
            except Exception as ex:
                msg = 'Does not support "{0}" storage mode.'.format(self._project_storage_type)
                raise DistributedDoesNotSupportStorage(msg)

    def sync_code(self):
        """

        :return:
        """
        self._logger.info("[ScanProject] Start syncing project code into the scan directory...")


        if self._project_type == 'online':  # online
            self._git.checkout_branch_sync_code(self._project_branch, self._force_sync_code)
            self._branch_commit = self._git.get_branch_last_commit_id()
            self._logger.info('[ScanProject] current branch commit:{0}, branch name:{1}'.format(
                self._branch_commit, self._project_branch)
            )
            cmd = " -R {0}/* {1}".format(self._project_path, self._paths_project_scan)
            self._logger.debug("[ScanProject] cp{0}".format(cmd))
            self.cp.exec_match(cmd=cmd)

        elif self._project_type == 'offline' and self._project_local_path:
            cmd = " -R {0}/* {1}".format(self._project_local_path, self._paths_project_scan)
            self._logger.debug("[ScanProject] cp{0}".format(cmd))
            self.cp.exec_match(cmd=cmd)

        else:  # offline
            self.__init_distributed()
            if self._project_storage_type in self.storage:
                if self._project_storage_type == 'local':  # TODO
                    pass
                elif self._project_storage_type == 'ftp':  # FTP
                    make_dir(self._project_path)
                    local_file = os.path.join(self._project_path, self._project_file_origin_name)
                    remote_file = urlparse(self._project_ssh).path
                    if not os.path.isfile(local_file):
                        self.storage['ftp'].download_file(local_file, remote_file)
                    unzip_cmd = ['/usr/bin/unzip', '-n', local_file, '-d', self._paths_project_scan]
                    self._logger.debug("[ScanProject] Start unzipping the file:[{0}]".format(' '.join(unzip_cmd)))
                    output, err = exec_cmd(' '.join(unzip_cmd))
                    self.storage['ftp'].close()
                    if err:
                        raise Exception(err)
            else:
                msg = 'Does not support "{0}" storage mode.'.format(self._project_storage_type)
                raise DistributedDoesNotSupportStorage(msg)

        self._logger.info("[ScanProject] Synchronization project code completion.")

    def clear_exclude(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self._logger.info("[ScanProject] Start executing exclusion rules...")
        exclude_dir = kwargs.get('exclude_dir', None)
        exclude_ext = kwargs.get('exclude_ext', None)
        exclude_file = kwargs.get('exclude_file', None)

        target = {
            'dir': [],
            'ext': [],
            'file': [],
        }

        if exclude_dir:
            if isinstance(exclude_dir, list):
                target['dir'].extend(exclude_dir)
            else:
                target['dir'].append(exclude_dir)

        if exclude_ext:
            if isinstance(exclude_ext, list):
                target['ext'].extend(exclude_ext)
            else:
                target['ext'].append(exclude_ext)

        if exclude_file:
            if isinstance(exclude_file, list):
                target['file'].extend(exclude_file)
            else:
                target['file'].append(exclude_file)

        for k, values in target.items():
            for v in values:
                if k == 'dir':
                    cmd = ' {0} -type d -name "{1}" | xargs rm -rf'.format(self._paths_project_scan, v.replace("/", ""))
                    self._logger.debug("[ScanProject] find{0}".format(cmd))
                    self.find.exec_match(cmd=cmd)
                elif k in ('file', 'ext'):
                    if not v.startswith('*'):
                        vv = '*{0}'.format(v)
                    else:
                        vv = v
                    cmd = ' {0} -type f -name "{1}" | xargs rm -rf'.format(self._paths_project_scan, vv)
                    self._logger.debug("[ScanProject] find{0}".format(cmd))
                    self.find.exec_match(cmd=cmd)
        self._logger.info("[ScanProject] Exclusion rule execution completed.")

    def sync_vuln(self):
        """

        :return:
        """
        try:
            # sync result
            risk_statistics = {
                'vulnerability': {
                    '1': 0,  # critical
                    '2': 0,  # high
                    '3': 0,  # medium
                    '4': 0,  # low
                },
                'bug': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                },
                'code smell': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                }
            }

            if self._task_status and self._sync_vuln_to_server:
                self._logger.info("[ScanProject] Start syncing scan results to the server...")
                result, rule_list, critical, high, medium, low, info, scope = [], [], 0, 0, 0, 0, 0, 0

                for _, vuln in kb.result[self.key].items():
                    result.append(vuln)
                    if len(result) % self.send_size == 0:
                        self._task_status.bulk_send_vulnerability(result)
                        result = []
                    if vuln['category'] in self._issue_statistic_type:
                        if vuln['risk_id'] == 1:
                            critical += 1
                        elif vuln['risk_id'] == 2:
                            high += 1
                        elif vuln['risk_id'] == 3:
                            medium += 1
                        elif vuln['risk_id'] == 4:
                            low += 1
                    else:
                        self._logger.debug("[ScanProject] [SKIP] '{0}' not in {1}.".format(
                            vuln['category'], self._issue_statistic_type)
                        )
                    # project scope
                    if vuln['category'].lower() in risk_statistics and vuln['rule_key'] not in rule_list:
                        if str(vuln['risk_id']) in risk_statistics[vuln['category']]:
                            rule_list.append(vuln['rule_key'])
                            risk_statistics[vuln['category']][str(vuln['risk_id'])] += 1

                if result:
                    self._task_status.bulk_send_vulnerability(result)

                scope = get_project_scope(risk_statistics)
                self._logger.info('[ScanProject] Project scope: [{0}]'.format(scope))

                self._task_status.update_complete(
                    critical=critical,
                    high=high,
                    medium=medium,
                    low=low,
                    info=info,
                    scope=scope,
                )

                self._logger.info("[ScanProject] Synchronization completed.".format(len(kb.result[self.key])))

            # dump result
            if self._result_file:
                dump = DumpReport(self._result_file)
                dump.save(kb.result[self.key])
                self._logger.info("[ScanProject] [+] Save the scan log to '{0}'.".format(self._log_file))
                self._logger.info("[ScanProject] [+] Save the scan results to '{0}', total: {1}.".format(
                    self._result_file,
                    len(kb.result[self.key]))
                )

            # upload result
            self.upload_result_log()
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            self._logger.error(ex)
            self.update_scan_failed_status(ex)

    def analysis_component(self):
        """
        analysis component
        :return:
        """
        try:
            self._logger.info("[ScanProject] Start analyzing components...")
            project_size = get_dir_size(self._paths_project_scan, _logger=self._logger)
            if project_size:
                self._statistics['size'] = int(project_size)
            if self._statistics['size'] == 0:
                msg = 'Scan directory "{0}" is empty, please confirm that the ' \
                      'scan parameters are correct.'.format(self._paths_project_scan)
                raise ScanDirectoryIsEmpty(msg)

            # TODO 如果当前的hash已经存在，直接退出扫描。
            c = ClocDetector(code_dir=self._paths_project_scan, skip_check_new_version=True)
            c.start()
            results = c.getResult

            if results:
                if results['cloc']:
                    language = None
                    max_file, result_lang, code_total = 0, [], 0

                    for k, v in results['cloc'].items():
                        if k in ('header', 'SUM'):
                            if k == 'SUM':
                                code_total = v['code']
                            continue

                        result_lang.append(k)
                        if v['nFiles'] > max_file:
                            max_file = v['nFiles']
                            language = k

                        self._statistics['file'].append({
                            'language': k,
                            'files': v['nFiles'],
                            'blank': v['blank'],
                            'comment': v['comment'],
                            'code': v['code']
                        })

                    # FIXME 动态语言为主
                    for lang in ('Java', 'Vuejs', 'Python'):
                        if lang in result_lang:
                            language = lang
                    msg = '[ScanProject] Project code line: [{0}], language: [{1}], size: [{2}] KB'.format(
                        code_total, language, self._statistics['size']
                    )
                    self._logger.info(msg)
                    self._logger.debug(self._statistics['file'])
                    self._statistics['total'] = code_total
                    self._statistics['language'] = language

                    if self._task_status and self._sync_vuln_to_server:
                        self._task_status.bulk_send_statistic(
                            size=self._statistics['size'],
                            total=code_total,
                            lang=language,
                            statistics=self._statistics['file']
                        )
                        self._task_status.update_statistics(
                            commit_hash=self.get_last_commit(),
                            reason=msg,
                        )
                if results['depends']:
                    result = []
                    for language in results['depends']:
                        for k, v in language.items():
                            for item in v:
                                self._statistics['depends'].append(item)
                                self._logger.debug("[ScanProject] [+] group: [{0}], name: [{1}], version: [{2}], "
                                                   "origin: [{3}]".format(
                                    item['tag'], item['name'], item['version'], item['origin'])
                                )
                                if self._task_status and self._sync_vuln_to_server:
                                    result.append(item)
                                    if len(result) % self.send_size == 0:
                                        self._task_status.bulk_send_component(result)
                                        result = []

                    if self._task_status and result and self._sync_vuln_to_server:
                        self._task_status.bulk_send_component(result)
                else:
                    self._logger.warning('[ScanProject] No related dependencies found!!!')

                if self._task_status and self._sync_vuln_to_server:
                    self._task_status.update_scanning()

        except CodeDirIsNoneException as ex:
            self._logger.warning(ex)
        except Exception as ex:
            self._logger.error(ex)
            raise ex

    def update_scan_failed_status(self, ex):
        """

        :param ex:
        :return:
        """
        self._logger.warning(ex)
        if self._task_status and self._sync_vuln_to_server:
            self._task_status.update_failed(reason=str(ex))

    def update_scan_message(self, title, reason=None, level=4):
        """

        :param title:
        :param reason:
        :param level:
        :return:
        """
        if self._task_status and self._sync_vuln_to_server:
            self._task_status.update_scan_message(title=title, reason=reason, level=level)

    def update_scan_engine_status(self, engine_id, action):
        """

        :param engine_id: 引擎 ID
        :param action: 黑名单、白名单
        :return:
        """
        message = ''
        if action == 'blacklist':
            if engine_id == 1:
                message = '[SonarScanner] 正在执行黑名单检测...'
            elif engine_id == 2:
                message = '[RuleScanner] 正在执行黑名单检测...'
            elif engine_id == 3:
                message = '[PluginScanner] 正在执行黑名单检测...'
        else:
            if engine_id == 1:
                message = '[SonarScanner] 正在执行白名单过滤...'
            elif engine_id == 2:
                message = '[RuleScanner] 正在执行白名单过滤...'
            elif engine_id == 3:
                message = '[PluginScanner] 正在执行白名单过滤...'

        self._logger.info(message)
        if self._task_status and self._sync_vuln_to_server:
            self._task_status.update_scan_message(title=message)
