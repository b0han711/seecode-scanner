# coding: utf-8
import subprocess

import os
import re

from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.data import logger as _logger
from seecode_scanner.lib.core.execptions import GitDoesNotPermissionException
from seecode_scanner.lib.core.execptions import CheckoutBranchException


class GitOperator(object):

    def __init__(self, project_path, git_url, logger=None):
        """
        :param project_path:
        :param git_url:
        :param logger:
        """
        git_search_path = ('git', '/usr/bin/git', '/usr/local/bin/git', '/opt/local/bin/git')
        self.project_path = project_path
        self.git_url = git_url
        self.logger = logger or _logger
        self.git_path = ''
        regex = re.compile(r'git version [0-9]*\.[0-9]*\.[0-9]')
        self.current_branch = None
        self.local_branch_list = []

        for git_path in git_search_path:
            try:
                p = subprocess.Popen([git_path, '--version'], bufsize=1024, stdout=subprocess.PIPE)
                self.git_path = git_path
                break
            except (OSError, FileNotFoundError):
                pass
        else:
            msg = '[GitOperator] git program was not found in path. PATH is : {0}'.format(os.getenv('PATH'))
            self.logger.error(msg)
            raise Exception(msg)
        self._git_last_output = bytes.decode(p.communicate()[0])
        if regex.match(self._git_last_output):
            self.logger.debug(self._git_last_output.strip())

    def file_exists_in_repo(self, filename="sonar-project.properties"):
        """
        检测文件是否在git仓库中
        :param filename: 要检测的文件
        :return:
        """
        result = False
        self.logger.debug("[GitOperator] Detects whether the '{0}' file is in the git repository...".format(filename))
        output, _ = exec_cmd(' '.join(['cd', self.project_path, '&&', self.git_path, 'ls-files', filename, "--error-unmatch;"]))

        if output and filename == output.strip().decode("utf-8"):
            result = True
            self.logger.info("[GitOperator] [+] Found '{0}' files in the gitlab project.".format(filename))
        else:
            self.logger.warning("[GitOperator] [-] '{0}' file not found.".format(filename))

        return result

    def checkout_file(self, filename):
        """
        checkout 文件
        :param filename:
        :return:
        """
        cmd = ['cd', self.project_path, '&&', self.git_path, 'checkout', filename]
        self.logger.debug('[GitOperator] {0}'.format(' '.join(cmd)))
        exec_cmd(' '.join(cmd))

    def get_branch_last_commit_id(self):
        """
        得到当前分支的最后一次 commit id
        :return:
        """
        cmd = ['cd', self.project_path, '&&', self.git_path, 'log', '--pretty=oneline', '|', 'awk', '\'{print($1)}\'', '|', 'head -n 1']
        self.logger.debug('[GitOperator] {0}'.format(' '.join(cmd)))
        result, _ = exec_cmd(' '.join(cmd))

        return result.strip().decode("utf-8")

    def get_all_local_branch(self):
        """
        获取本地的所有分支
        :return:
        """
        cmd = ['cd', self.project_path, '&&', self.git_path, 'branch']
        self.logger.debug('[GitOperator] {0}'.format(' '.join(cmd)))
        result, _ = exec_cmd(' '.join(cmd))

        if result:
            result = result.decode("utf-8").split("\n")
            self.local_branch_list = [r.strip() for r in result if r]

    def get_commit_author(self, git_file_path):
        """
        获得git文件中的最后一次提交作者
        :param git_file_path: 要检测的文件
        :return:
        """
        cmd = ['cd', self.project_path, '&&', self.git_path, 'log', '-n', '1', git_file_path, '|', 'sed', '-n', '\'2,1p\'']
        self.logger.debug('[GitOperator] {0}'.format(' '.join(cmd)))
        result, _ = exec_cmd(' '.join(cmd))
        if result:
            result = result.strip().decode("utf-8").replace('Author:', '')
        return result

    def get_current_branch(self):
        """
        获得当前程序的分支
        :return:
        """
        cmd = ['cd', self.project_path, '&&', self.git_path, 'symbolic-ref', '--short', '-q', 'HEAD']
        result, _ = exec_cmd(' '.join(cmd))
        self.logger.debug('[GitOperator] {0}'.format(' '.join(cmd)))
        if result:
            self.current_branch = result.strip().decode("utf-8")
        return self.current_branch

    def checkout_branch_sync_code(self, branch_name, sync_code=False):
        """
        切换分支同步代码
        :param branch_name:
        :param sync_code:
        :return:
        """
        # 初始化并克隆代码
        git_config_path = os.path.join(self.project_path, '.git')
        if not os.path.isdir(git_config_path):
            self.logger.info('[GitOperator] git clone project to "{0}" ...'.format(self.project_path))
            cmd = [self.git_path, 'clone', '--depth 1', self.git_url, self.project_path]
            self.logger.info("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
            _, err = exec_cmd(' '.join(cmd))
            if err and 'fatal: Could not read from remote repository.' in err.decode('utf-8'):
                raise GitDoesNotPermissionException('克隆项目代码失败，当前没有权限。{0}'.format(err))
            cmd = ['cd', self.project_path, '&&', self.git_path, 'remote', 'add', 'upstream', self.git_url, '&&', self.git_path, 'fetch', '--all', '-p',]
            self.logger.info("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
            exec_cmd(' '.join(cmd))

        # 解决多个分支切换导致的文件冲突问题
        cmd = ['cd', self.project_path, '&&', self.git_path, 'reset', '.', '&&', self.git_path, 'checkout', '.', '&&', self.git_path, 'stash']
        self.logger.debug("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
        exec_cmd(' '.join(cmd))

        self.get_all_local_branch()
        if branch_name in self.local_branch_list:
            cmd = ['cd', self.project_path, '&&', self.git_path, 'checkout', branch_name]
            self.logger.debug("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
            exec_cmd(' '.join(cmd))

        if sync_code:  # fetch && pull
            self.logger.info("[GitOperator] Force update of local code...")
            cmd = ['cd', self.project_path, '&&', self.git_path, 'fetch', '--all', '-p', '&&', self.git_path, 'pull']
            self.logger.debug("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
            exec_cmd(' '.join(cmd))

        # 验证扫描分支是否一致
        current_branch = self.get_current_branch()
        if current_branch.strip() != branch_name.strip():  # 判断本地是否存在分支
            self.logger.info('[GitOperator] Start switching branches, current branch: [{0}], target branch: [{1}].'.format(
                current_branch.strip(), branch_name.strip()
            ))
            cmd = ['cd', self.project_path, '&&', self.git_path, 'checkout', '-b', branch_name, 'remotes/upstream/{0}'.format(branch_name)]
            self.logger.debug("[GitOperator] Start executing commands: '{0}'".format(' '.join(cmd)))
            _last_output, _ = exec_cmd(' '.join(cmd))
            current_branch = self.get_current_branch()
            if current_branch != branch_name.strip():
                raise CheckoutBranchException('切换分支失败! {0}'.format(_))
        self.logger.info('[GitOperator] Code synchronization completed.')
        return True
