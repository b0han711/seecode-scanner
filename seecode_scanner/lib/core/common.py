#!/usr/bin/env python
# coding: utf-8

import socket
import os
import subprocess
import glob
import hashlib
import shutil
import math
import re

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pytz import timezone

from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.settings import BASIC_SCOPE


def exec_cmd(cmd):
    """
    执行一个命令并返回
    :param cmd:
    :return:
    """
    logger.debug(cmd)
    p = subprocess.Popen(
        cmd,
        bufsize=100000,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True,
    )
    p.wait()
    out, cmd_err = p.communicate()
    if p.returncode != 0:
        logger.warning('cmd: [{0}], error: [{1}], return code: [{2}]'.format(
            cmd, cmd_err.strip().decode("utf-8"), p.returncode
        ))

    return out, cmd_err


def parse_int(str_value, default_value=0):
    """
    转换成int
    :param str_value:
    :param default_value:
    :return:
    """
    if str_value:
        try:
            result = int(str_value)
        except (ValueError, TypeError):
            result = default_value
    else:
        result = default_value
    return result


def parse_int_or_str(str_value):
    """
    :param str_value:
    :return:
    """
    result = None
    if str_value:
        if isinstance(str_value, int):
            result = str_value
        elif isinstance(str_value, str) or isinstance(str_value, bytes):
            if isinstance(str_value, bytes):
                result = str_value.decode("utf-8").strip()
            else:
                result = str_value.strip()
            try:
                result = int(result)
            except (ValueError, TypeError):
                pass
    return result


def parse_bool(str_value):
    """
    
    :param str_value:
    :return: 
    """
    result = False
    if str_value:
        str_value = parse_int(str_value, str_value)
        if isinstance(str_value, bool):
            result = str_value

        if isinstance(str_value, int):
            if str_value < 1:
                result = False
            else:
                result = True

        if isinstance(str_value, bytes):
            str_value = str_value.decode("utf-8")

        if isinstance(str_value, str):
            str_value = str_value.strip()
            right_value = ['true', 'on']
            if str_value.lower().strip() in right_value:
                result = True

    return result


def strip(str_param, display_type=None):
    """

    :param str_param:
    :param display_type:
    :return:
    """
    result = str_param
    if str_param:
        if isinstance(str_param, str) or isinstance(str_param, bytes):
            result = str_param.strip()
            if display_type:
                if display_type.strip() == 'lower':
                    result = result.lower()
                elif display_type.strip() == 'upper':
                    result = result.upper()
    return result


def parse_category(str_value):
    """

    :param str_value:
    :return:
    """
    result = str_value
    if str_value:
        str_value = str_value.replace("_", " ")
        result = str_value.lower()

    return result


def make_dir(paths):
    """
    创建路径
    :param paths:
    :return:
    """
    try:
        if isinstance(paths, list):
            for item in paths:
                if item and not os.path.isdir(item):
                    os.makedirs(item)
        if isinstance(paths, str):
            if paths and not os.path.isdir(paths):
                os.makedirs(paths)
    except Exception as ex:
        pass


def get_localhost_ip(domain='example.com'):
    """
    获取本机IP
    :return:
    """
    ip = ""
    try:
        port = 80
        if ':' in domain:
            domain, port = domain.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((domain, int(port)))
        ip = s.getsockname()[0]

    except:
        pass
    finally:
        s.close()

    if not ip:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except:
            pass

    return ip


def get_hostname():
    """
    获取本地主机名称
    :return:
    """
    return socket.gethostname()


def check_ip(ip_addr):
    """

    :param ip_addr:
    :return:
    """
    try:
        socket.inet_aton(ip_addr)
        return True
    except:
        return False


def get_dir_size(path, _logger=None):
    """
    获得项目大小
    :param path:
    :param _logger:
    :return:
    """

    result = 0
    log = _logger or logger
    try:
        if os.path.isdir(path):
            cmd = ["/usr/bin/du", "-shk", path, "|", "awk '{print($1)}'"]
            log.debug('Query project size, execute cmd: [{0}]'.format(' '.join(cmd)))
            output, err = exec_cmd(' '.join(cmd))
            if output:
                result = parse_int_or_str(output)
    except Exception as ex:
        log.error(ex)
    return result


def get_line_content(file, start_line, count=1):
    """
    获取文件指定行内容
    :param file:
    :param start_line: 起始行
    :param count: 读取行数
    :return:
    """

    result = []
    start_line = parse_int(start_line, 0)
    count = parse_int(count, 1)

    if start_line <= 1:
        start_line = 1

    if count < 1:
        count = 1
    contents = []
    if isinstance(file, list):
        contents = file
    elif isinstance(file, str):
        if os.path.isfile(file):
            with open(file, 'r') as fp:
                contents = fp.readlines()

    i = 0
    is_start = False
    for item in contents:
        i += 1
        if i == start_line:
            if isinstance(item, bytes):
                result.append('{0}\n'.format(item.rstrip().decode("utf-8")))
            else:
                result.append('{0}\n'.format(item.rstrip()))
            is_start = True
            continue
        if is_start:
            if isinstance(item, bytes):
                result.append('{0}\n'.format(item.rstrip().decode("utf-8")))
            else:
                result.append('{0}\n'.format(item.rstrip()))

        if len(result) >= count:
            is_start = False

    return result


def get_lang(lang_list, lang):
    """

    :param lang_list:
    :param lang:
    :return:
    """
    for item in lang_list:
        if lang.lower() == item[1].lower():
            return item[0]


def get_file_list(code_dir=None, include_ext=[], exclude_ext=[]):
    """
    获得文件夹下的指定扩展文件
    :param code_dir:
    :param include_ext:
    :param exclude_ext:
    :return:
    """
    def is_filter_dir(dir_name, ex_dirs=[]):
        """
        过滤目录
        :param dir_name:
        :param ex_dirs:
        :return:
        """
        for item in ex_dirs:
            if item in dir_name:
                return True

    dir_list = []
    result = []
    for fpath, dirs, fs in os.walk(code_dir):
        if is_filter_dir(fpath, exclude_ext):
            continue
        dir_list.append(os.path.join(fpath))

    for _dir in set(dir_list):
        for _ext in include_ext:
            result.extend(glob.glob(os.path.join(_dir, _ext)))

    return set(result)


def get_str_line(search_str, content):
    """

    :param search_str:
    :param content:
    :return:
    """
    lineNum = 0
    if content:
        if isinstance(content, list):
            for item in content:
                lineNum += 1
                if search_str in item.decode("utf-8"):
                    return lineNum
        else:
            for item in content.split('\n'):
                lineNum += 1
                if search_str in item.decode("utf-8"):
                    return lineNum
    return lineNum


def get_risk_sonar_label(risk):
    """

    :param risk:
    :return:
    """
    if risk == 1:
        return 'BLOCKER'
    elif risk == 2:
        return 'CRITICAL'
    elif risk == 3:
        return 'MAJOR'
    elif risk == 4:
        return 'BLOCKER'
    else:
        return ''


def get_risk_by_severity(severity):
    """

    :param severity:
             (1, u"Blocker"),  # 最高等级，阻碍的
             (2, u"Critical"),  # 高等级，极为严重的
             (3, u"Major"),  # 较高等级，主要的；默认级别。
             (4, u"Minor"),  # 较低等级
             (5, u"Info"),  # 低等级
    :return:
    """
    if not severity:
        risk = 4
    else:
        if severity.lower() in ('blocker', 'critical'):
            risk = 1
        elif severity.lower() in ('major',):
            risk = 2
        elif severity.lower() in ('minor',):
            risk = 3
        else:
            risk = 4
    return risk


def get_issue_type_by_sonar(type_str):
    """

    :param type_str:
        (1, u"Bug"),  # 缺陷
        (2, u"Code Smell"),  # 代码坏味道
        (3, u"Vulnerability"),  # 易受攻击
    :return:
    """
    if not type_str:
        issue_type = 3
    else:
        if isinstance(type_str, str):
            type_str = type_str.strip().replace('_', ' ')
            if type_str.lower() in ('bug',):
                issue_type = 1
            elif type_str.lower() in ('code smell',):
                issue_type = 2
            elif type_str.lower() in ('vulnerability',):
                issue_type = 3
        else:
            issue_type = 3

    return issue_type


def get_week():
    today = datetime.today()
    weekday = today.weekday()

    start = today + timedelta(0 - weekday)
    end = today + timedelta(6 - weekday)

    r_start = datetime(start.year, start.month, start.day)
    r_end = datetime(start.year, start.month, end.day)

    return r_start, r_end


def get_beijing_iso_datetime(datetime_obj):
    """

    :param datetime_obj:
    :return:
    """
    tz = timezone('Asia/Shanghai')
    date_str = datetime_obj.replace(tzinfo=tz).isoformat()

    if date_str:
        iso_8601, _ = date_str.split('.')
        return '{0}+0800'.format(iso_8601)

    return None


def hash_md5(hash_str):
    """

    :param hash_str:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(hash_str.encode("utf-8"))
    return md5.hexdigest()


def hash_md5_file(file_path):
    """

    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as fp:
            return hash_md5(fp.read())


def get_total_page(total, page_size=200):
    """

    :param total:
    :param page_size:
    :return:
    """
    return math.ceil(int(total)/int(page_size))


def clean_dir(target_path):
    """

    :param target_path:
    :return:
    """

    if os.path.isdir(target_path):
        try:
            shutil.rmtree(target_path)
        except:
            import traceback;traceback.print_exc()


def checkFile(filename, raiseOnError=True):
    """
    Checks for file existence and readability
    >>> checkFile(__file__)
    True
    """

    valid = True

    if filename:
        filename = filename.strip('"\'')

    try:
        if filename is None or not os.path.isfile(filename):
            valid = False
    except:
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid and raiseOnError:
        raise Exception("unable to read file '%s'" % filename)

    return valid


def str_to_list(content, separator=',', prefix=None):
    """

    :param content:
    :param separator:
    :param prefix:
    :return:
    """
    result = []
    if content:
        if isinstance(content, str):
            result = [_.strip() for _ in content.split(separator) if _]
        if prefix:
            _result = []
            for i in result:
                if i.startswith('*'):
                    i = i.replace('*', '')
                if not i.startswith(prefix):
                    _result.append('{0}{1}'.format(prefix, i))
                else:
                    _result.append(i)
            result = _result

    return result


def find_text(parent_node, sub_node_name, default_value=''):
    """

    :param parent_node:
    :param sub_node_name:
    :param default_value:
    :return:
    """
    result = default_value
    if parent_node:
        sub_node = parent_node.find(sub_node_name)
        if isinstance(sub_node, ET.Element):
            result = sub_node.text or default_value
    return result


def get_project_scope(risk_statistics):
    """

    :param risk_statistics: {
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
    :return:
    """
    def calculate_highest_risk(risk_data, risk_type):
        total_scope = 0
        for i in range(1, 5):
            risk_id = str(i)
            if risk_id in risk_data and risk_data[risk_id] > 0:
                scope = BASIC_SCOPE[risk_type][risk_id]['scope'] * risk_data[risk_id]
                min_scope = BASIC_SCOPE[risk_type][risk_id]['min']
                max_scope = BASIC_SCOPE[risk_type][risk_id]['max']
                if scope > 0:
                    if scope < min_scope:
                        scope += min_scope
                    if scope > max_scope:
                        scope = max_scope
                    total_scope += scope
                    break

        return total_scope

    total_scope = 0.0
    # vulnerability
    if 'vulnerability' in risk_statistics:
        total_scope += BASIC_SCOPE['vulnerability']['basic']
        scope = calculate_highest_risk(risk_statistics['vulnerability'], 'vulnerability')
        total_scope += scope
        if total_scope > 400.0:  # 超出范围
            return 400.0
        elif total_scope == 300:  # 没有风险
            total_scope = 0
        elif total_scope > 300:  # 危险
            return total_scope

    # bug
    if 'bug' in risk_statistics:
        total_scope += BASIC_SCOPE['bug']['basic']
        scope = calculate_highest_risk(risk_statistics['bug'], 'bug')
        total_scope += scope
        if total_scope > 300.0:  # 超出范围
            return 300.0
        elif total_scope == 200:  # 没有警告
            total_scope = 0
        elif total_scope > 200:  # 警告
            return total_scope

    # code smell
    if 'code smell' in risk_statistics:
        total_scope += BASIC_SCOPE['code smell']['basic']
        scope = calculate_highest_risk(risk_statistics['code smell'], 'code smell')
        total_scope += scope
        if total_scope <= 100:
            return 200.0

        if total_scope > 200.0:  # 超出范围
            return 25.0
        elif total_scope == 100:  # 没有安全
            total_scope = 200
        elif total_scope > 100:  # 安全
            return total_scope

    if total_scope == 0:
        total_scope = 200.0  # 安全
    return total_scope


def get_git_author(last_commit):
    """

    :param last_commit:
    :return:
    """
    author, author_email = '', ''
    if last_commit and not last_commit.startswith("Merge"):
        author_email = re.search(r'<(.+?)>', last_commit, re.I)
        if author_email:
            origin_str = author_email.group(0)
            author_email = author_email.group(1)
            author = strip(last_commit.replace(origin_str, ''))
    return author, author_email


def get_python_path():
    pwd = os.environ.get('PWD')
    virtual_env = os.environ.get('VIRTUAL_ENV')
    python_path = None
    if pwd:
        python_path = os.path.join(pwd, 'bin', 'python')
        if not os.path.isfile(python_path):
            python_path = None

    if virtual_env:
        python_path = os.path.join(virtual_env, 'bin', 'python')
        if not os.path.isfile(python_path):
            python_path = None

    return python_path or 'python'
