#!/usr/bin/env python

optDict = {
    # Family: {"parameter name": "parameter datatype"},
    # --OR--
    # Family: {"parameter name": ("parameter datatype", "category name used for common outputs feature")},

    "scan": {
        "template": "string",
        "threads": "integer",
        "work_dir": "string",
        "project_name": "string",
        "project_path": "string",
        "project_type": "string",
        "project_branch": "string",
        "project_upload_type": "string",
        "project_file_origin_name": "string",
        "project_file_hash": "string",
        "application_name": "string",
        "application_key": "string",
        "group_name": "string",
        "group_path": "string",
        "group_key": "string",
        "output_path": "string",
        "output_format": "string",
    },

    "agent": {
        "monitor_url": "string",
        "enable_agent_monitor": "boolean",
        "upgrade_url": "string",
        "enable_agent_upgrade": "boolean",
        "task_url": "string",
        "enable_agent_task": "boolean",
        "config": "string",
    },

    "distributed": {
        "task_id": "integer",
        "ftp_host": "string",
        "ftp_port": "integer",
        "ftp_username": "string",
        "ftp_password": "string",
        "ftp_path": "string",
    },

    "server": {
        "domain": "integer",
        "token": "string",
        "celery_broker_url": "string",
    },

    "cache": {
        "redis_broker_url": "string",
        "memcached_broker_url": "string",
    }
}
