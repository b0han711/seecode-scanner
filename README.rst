
SeeCode Scanner
====================

.. image:: https://img.shields.io/travis/seecode-audit/seecode-scanner/master.svg?label=travis-ci
   :alt: 
   :target: https://travis-ci.org/seecode-audit/seecode-scanner

.. image:: https://img.shields.io/badge/python-3.6|3.7-brightgreen.svg
    :alt: 
    :target: https://www.python.org/

.. image:: https://img.shields.io/github/issues/seecode-audit/seecode-scanner.svg
    :alt: GitHub issues
    :target: https://github.com/seecode-audit/seecode-scanner/issues

.. image:: https://img.shields.io/github/forks/seecode-audit/seecode-scanner.svg
    :alt: GitHub forks
    :target: https://github.com/seecode-audit/seecode-scannernetwork

.. image:: https://img.shields.io/github/stars/seecode-audit/seecode-scanner.svg
    :alt: GitHub stars
    :target: https://github.com/Mseecode-audit/seecode-scanner/stargazers

.. image:: https://img.shields.io/github/license/seecode-audit/seecode-scanner.svg
    :alt: GitHub license
    :target: https://github.com/seecode-audit/seecode-scanner/blob/master/LICENSE


.. rtd-inclusion-marker-do-not-remove

``seecode-scanner`` 是一款开源可独立运行的 SAST 代码检测工具，其支持命令行下对离线项目（本地项目）扫描；也可结合 SeeCode Audit 对线上（如：GitLab、GitHub）项目进行分布式扫描。

``seecode-scanner`` 也是一个扫描引擎框架，您可以包装任意的扫描引擎集成到该工具中， ``seecode-scanner`` 默认集成了三个引擎： SonarScanner、RuleScanner、PluginScanner。通过编写不同的扫描模板，来满足您在不同场景下的代码检测需求。


**主要功能特点：**

- **引擎可扩展**

    您可以编写自己的扫描引擎来集成到该工具中， 如：`PMD <https://github.com/pmd/pmd>`_ 、`TscanCode <https://github.com/Tencent/TscanCode>`_ 等开源的检测工具。

- **扫描配置灵活**

    您可以创建不同的扫描模板，来定制您的扫描需求，如：项目依赖组件漏洞、检测代码质量等。

- **支持单机/多节点/Docker部署**

    **单机**：通过命令行手动触发扫描；

    **分布式**：使用了 Celery 框架，进行分布式部署扫描；

    **Docker**：您可以通过 Dockfile 一键来部署您的扫描工具，方便快捷。
    
    可通过 FTP、AWS(TODO)等方式来存储扫描结果与日志。

- **依赖组件识别**

    工具使用 `clocwalk <https://github.com/seecode-audit/clocwalk>`_ 进行组件分析，默认支持：Java Maven、NodeJs、pip、Ruby 组件分析。

- **传输安全**

    支持与服务端通信内容 RSA 非对称加密，保证传输内容安全。

- **代码质量保证**

  - 单元测试覆盖率 70%；
  - 功能测试完成：规则引擎、Sonar 引擎测试，详情请查看 `tests <https://github.com/seecode-audit/seecode-scanner>`_ 。


.. Note:: seecode-scanner 是采用 python3 语言开发， 目前只支持 Linux 平台，建议您使用 CentOS 7 来安装部署。


1 使用说明
------------

1.1 安装
^^^^^^^^^^^

您可以通过以下命令进行安装：

.. code-block:: console

    $ pip install seecode-scanner

或者直接使用 cli.py 脚本来运行：

.. code-block:: console

    $ cd seecode_scanner
    $ python3 cli.py


1.2 配置
^^^^^^^^^^^

seecode_scanner.yml 是 seecode-scanner 的核心配置文件，默认路径为 /etc/seecode_scanner.yml 下， 其配置内容主要是与 SeeCode Audit
的服务端相关，本地测试使用可以不用配置。

.. code-block:: console

    $ vim /etc/seecode_scanner.yml

其内容如下，详细参数说明请参考 `系统配置 <docs/conf/core.rst>`_ 章节

.. code-block:: yaml

    server:
      domain: "http://seecode.com"
      api_uri: "/api/v2/"
      token: "dca58d563917b9325252f8a4b6c57e7331349052"
      public_key_path:
      private_key_path:
    
    celery:
      broker_url: ""
      timezone: "Asia/Shanghai"
      c_force_root: False
      task_timeout: 7200

    http:
      timeout: 10
      timeout_try: 3
      failed_try: 3
      try_status_code: 500, 502, 503
      proxies:
        http:
        https:
        socks5:
      headers:
        accept-encoding: "gzip, deflate"
    
    distributed:
      ftp:
        host: "192.168.1.1"
        port: 21
        username: "seecode"
        password: "test1234"
        path: "/home/seecode/"


1.3 使用
^^^^^^^^^^^

1). 扫描本地项目:

   .. code-block:: console

       $ seecode-scanner --scan-path /tmp/java_demo --name java_demo -o java_demo.json

2). 使用项目配置扫描:

   .. code-block:: console

       $ seecode-scanner -c java_demo.yml


3). 使用 Celery 扫描:

   .. code-block:: console

       $ seecode-scanner --celery



2 命令行操作
---------------


.. code-block:: console

    $ python cli.py

    -------------------------------------------------------------------------------------------
          ____     U _____ u U _____ u    ____     U  ___ u   ____    U _____ u
         / __"| u  \| ___"|/ \| ___"|/ U /"___|     \/"_ \/  |  _"\   \| ___"|/
        <\___ \/    |  _|"    |  _|"   \| | u       | | | | /| | | |   |  _|"
         u___) |    | |___    | |___    | |/__  .-,_| |_| | U| |_| |\  | |___
         |____/>>   |_____|   |_____|    \____|  \_)-\___/   |____/ u  |_____|
          )(  (__)  <<   >>   <<   >>   _// \\        \\      |||_     <<   >>
         (__)      (__) (__) (__) (__) (__)(__)      (__)    (__)_)   (__) (__)
                  ____        ____      _        _   _       _   _     U _____ u    ____
                 / __"| u  U /"___| U  /"\  u   | \ |"|     | \ |"|    \| ___"|/ U |  _"\ u
                <\___ \/   \| | u    \/ _ \/   <|  \| |>   <|  \| |>    |  _|"    \| |_) |/
                 u___) |    | |/__   / ___ \   U| |\  |u   U| |\  |u    | |___     |  _ <
                 |____/>>    \____| /_/   \_\   |_| \_|     |_| \_|     |_____|    |_| \_\
                  )(  (__)  _// \\   \\    >>   ||   \\,-.  ||   \\,-.  <<   >>    //   \\_
                 (__)      (__)(__) (__)  (__)  (_")  (_/   (_")  (_/  (__) (__)  (__)  (__)

                 SeeCode Audit  seecode-scanner/1.0.0-20190903 xsseroot#gmail.com

    -------------------------------------------------------------------------------------------

    usage: seecode-scanner [-h] [-v {warn,debug,info,error}] [--test]
                           [--no-banner] [--version] [--upgrade] [--monitor]
                           [-c CONFIG] [--scan-template TEMPLATE]
                           [--scan-threads THREADS] [--scan-path PROJECT_PATH]
                           [--name PROJECT_NAME] [--result-file RESULT_FILE]
                           [--celery] [--celery-concurrency CELERY_CONCURRENCY]
                           [--celery-name CELERY_NAME]
    
    optional arguments:
      -h, --help            show this help message and exit
      -v {warn,debug,info,error}
                            Verbosity level, default: info.
      --test, -t            Test the status of all system services, default:
                            False.
      --no-banner           Do not display banner information, default: False.
      --version             Show current software version.
      --upgrade             Connect to the server for scanning configuration
                            upgrade, default: False.
      --monitor             SeeCode Scanner client heartbeat monitoring service,
                            default: False.
    
    scan arguments:
      -c CONFIG             Project scan configuration file based on yaml format.
      --scan-template TEMPLATE
                            Scan the name of the template, default: normal
      --scan-threads THREADS
                            The number of threads when the engine scans, default:
                            20.
      --scan-path PROJECT_PATH, -p PROJECT_PATH
                            The absolute path of the item to be scanned.
      --name PROJECT_NAME, -n PROJECT_NAME
                            The name of the project to scan.
      --result-file RESULT_FILE, -o RESULT_FILE
                            Scan the path saved by the report.
    
    task arguments:
      --celery              Start celery's work tasks.
      --celery-concurrency CELERY_CONCURRENCY
                            Number of child processes processing the queue,
                            default: 4
      --celery-name CELERY_NAME
                            Set custom hostname, default: sca-1


2.1 基本配置
^^^^^^^^^^^^^^^^

``-v``
""""""""""""""""""

设置扫描日志级别，其范围为：warn、debug、info、error。


``--test``
""""""""""""""""""

测试扫描配置与各种参数检查。布尔型参数，默认为 False。

``--no-banner``
""""""""""""""""""

用于设置是否显示 banner 的开关。布尔型参数，默认为False。

``--upgrade``
""""""""""""""""""

用于升级扫描模板开关，需要 SeeCode Audit 服务支持，同时 seecode_scanner.yml 配置文件必须配置正确。布尔型参数，默认为 False。

``--monitor``
""""""""""""""""""

用于采集扫描节点的IP、版本号信息，发送到 SeeCode Audit 服务端。布尔型参数，默认为 False。

2.2 扫描配置
^^^^^^^^^^^^^^^^

``-c``
""""""""""""""""""""""""""

指定一个项目配置文件来进行扫描， 详细内容请参考 `项目配置 <docs/conf/project.rst>`_ 。

``--scan-template``
""""""""""""""""""""""""""

通过命令行来设置扫描模板，输入范围必须是在 profiles 文件夹下的 xml 文件名。系统默认包含三个模板：default、normal、component_scan。

``--scan-threads``
""""""""""""""""""""""""""

通过命令行来设置扫描使用的线程(协成)数，默认为 20 。

``--scan-path``
""""""""""""""""""""""""""

扫描本地项目的项目路径，参数必须结合 --name 参数一起使用。

``--name``
""""""""""""""""""""""""""

扫描本地项目时的项目名称，参数必须结合 --scan-path 参数一起使用。

``--result-file``
""""""""""""""""""""""""""

用于设置扫描结果的文件名称，其内容默认为 json 格式。

2.3 Celery 配置
^^^^^^^^^^^^^^^^^^

``--celery``
""""""""""""""""""""""""""

通过命令行来启动 celery 的扫描任务。布尔型参数，默认为 False。

``--celery-concurrency``
""""""""""""""""""""""""""

该参数等同于 celery 中的 -c 参数。整型参数，默认为 4。

``--celery-name``
""""""""""""""""""""""""""

该参数等同于 celery 中的 -n 参数。默认值为 sca1。

TODO
--------

**引擎集成**

* https://github.com/OWASP/wpBullet
* https://github.com/pmd/pmd
* https://github.com/Tencent/TscanCode

捐赠
--------

* BTC 地址：18F4VFDX2MCEXod7zjUF8NepUdAspEcJR8
* ETH 地址：0xB3Bc55F4AAa8E87D3675B547e31d3eEbb585175c
* HT 地址：0x952b4cd9f18126987fdbfab55e1ea72c5ae72e16
