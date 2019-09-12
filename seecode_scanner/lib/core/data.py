#!/usr/bin/python
# coding: utf-8

from seecode_scanner.lib.core.datatype import AttribDict
from seecode_scanner.lib.core.log import logger

# paths
paths = AttribDict()

# conf
conf = AttribDict()

conf.general = AttribDict()
conf.general.is_test = False
conf.general.config = False
conf.general.version = None
conf.general.services = []

conf.server = AttribDict()
conf.server.domain = None
conf.server.token = None
conf.server.public_key_path = None
conf.server.private_key_path = None

conf.celery = AttribDict()
conf.celery.enable = False
conf.celery.broker_url = ''
conf.celery.concurrency = 4
conf.celery.name = ''
conf.celery.timezone = 'Asia/Shanghai'
conf.celery.c_force_root = False

conf.http = AttribDict()
conf.http.timeout = 10
conf.http.timeout_try = 3
conf.http.failed_try = 3
conf.http.proxies = []
conf.http.headers = {}

conf.scan = AttribDict()
conf.scan.template = "default"
conf.scan.template_full_path = None
conf.scan.threads = 20
conf.scan.work_dir = None
conf.scan.log_level = None
conf.scan.task_id = None
conf.scan.project_name = None
conf.scan.project_web = None
conf.scan.project_ssh = None
conf.scan.project_branch = None
conf.scan.project_type = None
conf.scan.project_storage_type = None
conf.scan.project_file_origin_name = None
conf.scan.project_file_hash = None
conf.scan.project_path = None
conf.scan.group_name = None
conf.scan.group_key = None
conf.scan.result_file = None
conf.scan.result_format = 'json'
conf.scan.evidence_start_line_offset = -1
conf.scan.evidence_count = 5
conf.scan.force_sync_code = True
conf.scan.sync_vuln_to_server = False

conf.agent = AttribDict()
conf.agent.monitor_url = None
conf.agent.enable_monitor = False
conf.agent.upgrade_url = None
conf.agent.enable_upgrade = False
conf.agent.task_url = None
conf.agent.enable_task = False

conf.distributed = AttribDict()

# object to share within function and classes results
kb = AttribDict()

kb.profiles = {}
kb.result = {}
kb.profiles_time = {}

# logger
logger = logger
