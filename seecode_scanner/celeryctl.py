# coding: utf-8

import os

from celery import Celery
from celery import platforms

from seecode_scanner.lib.core.common import parse_bool
from seecode_scanner.lib.core.data import conf

celery_app = Celery('seecode_scanner')
C_FORCE_ROOT = parse_bool(os.getenv('SEECODE_C_FORCE_ROOT')) or conf.celery.c_force_root
CELERY_BROKER_URL = os.getenv('SEECODE_CELERY_BROKER_URL') or conf.celery.broker_url
SEECODE_CELERY_TIMEZONE = os.getenv('SEECODE_CELERY_TIMEZONE') or conf.celery.timezone

celery_app.conf.update(
    broker_url=CELERY_BROKER_URL,
    timezone=SEECODE_CELERY_TIMEZONE,
    task_serializer='pickle',
    accept_content=['pickle'],
    worker_pool_restarts=True,
    task_soft_time_limit=60 * 60 * 2,  # task timeout 2h
    enable_utc=False,
    worker_max_tasks_per_child=500,
    worker_max_memory_per_child=100000,  # 100MB
    broker_transport_options={'visibility_timeout': 3600 * 24 * 7},
    task_annotations={'seecode_scanner.tasks.scan.start': {'rate_limit': '20/s'}},
    imports=('seecode_scanner.tasks.scan',),
    task_routes={
        'seecode_scanner.tasks.scan.start': {'queue': 'seecode'},
    }
)

if C_FORCE_ROOT:
    platforms.C_FORCE_ROOT = True
