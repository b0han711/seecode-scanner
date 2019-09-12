# coding: utf-8

from celery.exceptions import SoftTimeLimitExceeded

from seecode_scanner.celeryctl import celery_app
from seecode_scanner.cli import start_scan
from seecode_scanner.lib.core.data import logger
from seecode_scanner.lib.core.option import init


@celery_app.task(ignore_result=True)
def start(**kwargs):
    """
    添加扫描任务
    :param kwargs: 任务配置
    :return:
    """
    pro = None
    try:
        init()
        result_file = '{0}.json'.format(kwargs.get("project_name"))
        kwargs['result_file'] = result_file
        pro = start_scan(**kwargs)
    except SoftTimeLimitExceeded as ex:
        logger.critical(ex)
        if pro:
            pro.update_scan_failed_status(ex)
    except Exception as ex:
        import traceback;traceback.print_exc()
        logger.critical(ex)
    except KeyboardInterrupt:
        logger.error("user aborted")
    except SystemExit:
        raise

    return False
