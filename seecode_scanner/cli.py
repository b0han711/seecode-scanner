#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals, absolute_import

import cProfile
import os
import sys
import time

BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, BASEDIR)

from seecode_scanner.lib.core.settings import IS_WIN
from seecode_scanner.lib.parse.cmdline import cmd_line
from seecode_scanner.lib.core.data import conf
from seecode_scanner.lib.core.option import init
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.data import kb
from seecode_scanner.lib.core.agent import AgentServices
from seecode_scanner.lib.core.common import get_python_path
from seecode_scanner.lib.controller.project import ScanProject
from seecode_scanner.lib.core.execptions import CodeBaseException
from seecode_scanner.lib.core.execptions import ScanDirectoryIsEmpty
from seecode_scanner.lib.core.option import _mergeOptions
from seecode_scanner.lib.core.upgrade import UpgradeManage

if IS_WIN:
    print("[-] Sorry, doesn't support Microsoft's windows operating system, please replace it with Linux system.")
    input("[-] Press any key to continue...")
    exit(0)


def start_scan(**kwargs):
    """

    :param kwargs:
    :return:
    """
    pro = None
    try:
        pro = ScanProject(
            task_id=kwargs.get("task_id"),
            template=kwargs.get("template"),
            template_full_path=kwargs.get("template_full_path"),
            threads=kwargs.get("threads"),
            log_level=kwargs.get("log_level"),
            work_dir=kwargs.get("work_dir"),
            project_name=kwargs.get("project_name"),
            project_local_path=kwargs.get("project_local_path"),
            project_branch=kwargs.get("project_branch"),
            project_ssh=kwargs.get("project_ssh"),
            project_web=kwargs.get("project_web"),
            project_type=kwargs.get("project_type"),
            project_storage_type=kwargs.get("project_storage_type"),
            project_file_origin_name=kwargs.get("project_file_origin_name"),
            project_file_hash=kwargs.get("project_file_hash"),
            group_name=kwargs.get("group_name"),
            group_key=kwargs.get("group_key"),
            evidence_start_line_offset=kwargs.get("evidence_start_line_offset"),
            evidence_count=kwargs.get("evidence_count"),
            result_file=kwargs.get("result_file"),
            result_format=kwargs.get("result_format"),
            sync_vuln_to_server=kwargs.get("sync_vuln_to_server"),
            force_sync_code=kwargs.get("force_sync_code"),
            is_cli_call=kwargs.get("is_cli_call", False),
        )

        try:
            profile = kb.profiles[pro.template_name]
            pro.sync_code()
            pro.clear_exclude(
                exclude_dir='.git',
            )
            pro.analysis_component()
            pro.clear_exclude(
                exclude_dir=profile.exclude_dir,
                exclude_ext=profile.exclude_ext,
                exclude_file=profile.exclude_file,
            )

            for name, engine in profile.engines.items():
                engine.start_component(pro)

            for name, engine in profile.engines.items():
                try:
                    pro.update_scan_engine_status(engine.key, 'blacklist')
                    engine.start_blacklist(pro)
                except CodeBaseException as ex:
                    pro.update_scan_failed_status(ex)

            for name, engine in profile.engines.items():
                pro.update_scan_engine_status(engine.key, 'whitelist')
                engine.start_whitelist(pro)

            pro.sync_vuln()

        except (ScanDirectoryIsEmpty, Exception) as ex:
            pro.update_scan_failed_status(ex)
            pro.upload_result_log()
        except CodeBaseException as ex:
            pro.update_scan_failed_status(ex)

        return pro

    except CodeBaseException as ex:
        import traceback;
        traceback.print_exc()
        logger.critical(ex)
        return pro


def main():
    """

    :return:
    """
    try:
        init()
        args = cmd_line()
        _mergeOptions(args, conf)
        t1 = time.time()
        if conf.agent.enable_monitor:
            agent = AgentServices()
            agent.start_monitor()
            exit(0)

        elif conf.general.enable_upgrade:
            um = UpgradeManage()
            um.start_upgrade()
            exit(0)

        elif conf.celery.enable:
            cmd_list = [
                'cd', BASEDIR, '&&', get_python_path(), '$(which celery)', 'worker', '-A',
                'seecode_scanner.celeryctl.celery_app', '-c',
                str(conf.celery.concurrency), '-Q', 'seecode', '-n', conf.celery.name
            ]
            logger.info(' '.join(cmd_list))
            os.system(' '.join(cmd_list))
            exit(0)

        elif conf.scan.project_path:
            if not all((args.project_path, args.project_name,)):
                print("[*] Missing '--scan-path, --name' key parameters.\n")
                exit(0)

        # scan
        start_scan(
            task_id=conf.scan.task_id,
            template=conf.scan.template,
            template_full_path=conf.scan.template_full_path,
            threads=conf.scan.threads,
            log_level=conf.scan.log_level,
            work_dir=conf.scan.work_dir,
            project_name=conf.scan.project_name,
            project_local_path=conf.scan.project_path,
            project_branch=conf.scan.project_branch,
            project_ssh=conf.scan.project_ssh,
            project_web=conf.scan.project_web,
            project_type=conf.scan.project_type,
            project_storage_type=conf.scan.project_storage_type,
            group_name=conf.scan.group_name,
            group_key=conf.scan.group_key,
            evidence_start_line_offset=conf.scan.evidence_start_line_offset,
            evidence_count=conf.scan.evidence_count,
            result_file=conf.scan.result_file,
            result_format=conf.scan.result_format,
            sync_vuln_to_server=conf.scan.sync_vuln_to_server,
            force_sync_code=conf.scan.force_sync_code,
            is_cli_call=True,
        )
        logger.info('Analysis completed, time consuming: {0}s'.format(round(time.time() - t1, 2)))
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        if conf.scan.log_level == 'debug':
            import traceback;
            traceback.print_exc()
        logger.critical(ex)
        exit(-1)
    except KeyboardInterrupt:
        logger.error("user aborted")

    except EOFError:
        logger.error("exit")

    except SystemExit:
        raise


if __name__ == '__main__':

    if conf.scan.log_level == 'debug':
        cProfile.run("main()")
    else:
        main()
