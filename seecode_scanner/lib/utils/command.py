# coding: utf-8

import os
import subprocess

from seecode_scanner.lib.core.common import exec_cmd
from seecode_scanner.lib.core.execptions import SystemCommandNotFound


class FindCMD(object):

    def __init__(self, search_path=('find', '/usr/bin/find', '/usr/local/bin/find')):
        """
        :param search_path:
        """
        self._path = ''

        for _path in search_path:
            try:
                p = subprocess.Popen(
                    [_path, '--version'],
                    bufsize=1024,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    close_fds=True,
                )
                self._path = _path
                break
            except (OSError, FileNotFoundError) as ex:
                raise ex
        else:
            raise SystemCommandNotFound(
                '[FindCMD] find program was not found in path. PATH is : {0}'.format(os.getenv('PATH'))
            )

    def exec_match(self, cmd, match_str=None):
        """
        :param cmd:
        :param match_str:
        :return:
        """
        result = False
        os.chdir("/tmp")
        if isinstance(cmd, list):
            cmd_str = '{0} {1}'.format(self._path, ' '.join(cmd))
        else:
            cmd_str = '{0} {1}'.format(self._path, cmd)

        output, _ = exec_cmd(cmd_str)

        if match_str and match_str in output.decode('utf-8'):
            result = True

        return result


class GrepCMD(object):

    def __init__(self, search_path=('grep', '/usr/bin/grep', '/usr/local/bin/grep')):
        """
        :param search_path:
        """
        self._path = ''

        for _path in search_path:
            try:
                p = subprocess.Popen(
                    [_path, '--version'],
                    bufsize=1024,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    close_fds=True,
                )
                self._path = _path
                break
            except (OSError, FileNotFoundError):
                pass
        else:
            raise SystemCommandNotFound(
                '[GrepCMD] grep program was not found in path. PATH is : {0}'.format(os.getenv('PATH'))
            )

    def exec_match(self, cmd, match_str=None):
        """
        :param cmd:
        :param match_str:
        :return:
        """
        result = False
        os.chdir("/tmp")
        if isinstance(cmd, list):
            cmd_str = '{0} {1}'.format(self._path, ' '.join(cmd))
        else:
            cmd_str = '{0} {1}'.format(self._path, cmd)

        output, _ = exec_cmd(cmd_str)

        if match_str and match_str in output.decode('utf-8'):
            result = True

        return result


class CopyCMD(object):

    def __init__(self, search_path=('cp', '/usr/bin/cp', '/usr/local/bin/cp')):
        """
        :param search_path:
        """
        self._path = ''

        for _path in search_path:
            try:
                p = subprocess.Popen(
                    [_path, '--version'],
                    bufsize=1024,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    close_fds=True,
                )
                self._path = _path
                break
            except (OSError, FileNotFoundError):
                pass
        else:
            raise SystemCommandNotFound(
                '[CopyCMD] cp program was not found in path. PATH is : {0}'.format(os.getenv('PATH'))
            )

    def exec_match(self, cmd, match_str=None):
        """
        :param cmd:
        :param match_str:
        :return:
        """
        result = False
        os.chdir("/tmp")
        if isinstance(cmd, list):
            cmd_str = '{0} {1}'.format(self._path, ' '.join(cmd))
        else:
            cmd_str = '{0} {1}'.format(self._path, cmd)

        output, _ = exec_cmd(cmd_str)

        if match_str and match_str in output.decode('utf-8'):
            result = True

        return result
