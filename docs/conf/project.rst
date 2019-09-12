
============
3 项目配置
============

项目扫描配置，主要是使用 yaml 文件来编写一个配置文件，方便 seecode-scanner 的 -c 参数来执行扫描。其可以省去繁琐的命令行参数和 Celery 的集成，更方便测试时使用。


3.1 配置格式
==============

其内容格式如下， 这一个线上(online)项目的扫描配置：

.. code-block:: yaml

	scan:
	  # 任务ID
	  task_id: 9527
	  # 扫描模板
	  template: "normal"
	  # 扫描线程数
	  threads: 20
	  # 日志
	  log_level: "debug"
	  # 工作目录
	  work_dir: "/data/seecode/"
	  # 项目 git 地址
	  project_ssh: "git@github.com:seecode-audit/vuln_java.git"
	  # web
	  project_web: "https://github.com/seecode-audit/vuln_java"
	  # 项目名称
	  project_name: "vuln_java"
	  # 分支名称
	  project_branch: "master"
	  # 项目类型： online， offline
	  project_type: "online"
	  # 上传方式: local, ftp, aws
	  project_storage_type: "local"
	  # 文件原始名称
	  project_file_origin_name: ""
	  # 文件MD5
	  project_file_hash: ""
	  # 分组名称
	  group_name: "seecode-audit"
	  # 分组key
	  group_key: "seecode-audit"
	  # 取证开始行偏移
	  evidence_start_line_offset: -1
	  # 取证行数
	  evidence_count: 5
	  # 强制同步线上代码
	  force_sync_code: True
	  # 同步漏洞到 server 需要与 task_id 参数一起使用
	  sync_vuln_to_server: True
	  # 结果格式
	  result_format: "json"
	  # 结果文件
	  result_file: "9527.json"


线下(offline)项目的扫描配置内容大致如下：

.. code-block:: yaml

	scan:
	  task_id: 184
	  template: "normal"
	  log_level: "debug"
	  work_dir: "/data/seecode/"
	  project_name: "xxxxx"
	  project_branch: "master"
	  project_ssh: "ftp://192.168.1.100:21/home/seecode/projects/XIANXIAXIANGMUZU/1566816638.zip"
	  project_web: ""
	  project_file_origin_name: "xxxxx.zip"
	  project_file_hash: "1b6d61ee077eb0b9c12465e24b388033"
	  group_name: "线下项目组"
	  group_key: "xianxiaxiangmuzu"
	  project_type: "offline"
	  project_storage_type: "ftp"
	  evidence_start_line_offset: -1
	  evidence_count: 5
	  result_file: "184.json"
	  sync_vuln_to_server: True
	  force_sync_code: False



3.2 参数说明
==============

scan 是 yaml 的主节点，默认配置文件中仅存在这一个主节点。

``task_id``
--------------------

扫描任务的 id，该 id 来自 SeeCode Audit 系统中下发的扫描任务 id，一般形式为整型。


``template``
--------------------

扫描模板名称，系统默认自带了三个扫描模板: default、normal、component_scan。

  - default 扫描模板包含了：RuleScanner、PluginScanner 两个扫描引擎
  - normal 扫描模板包含了：RuleScanner、PluginScanner、SonarScanner 三个扫描引擎
  - component_scan 扫描模板包含了：RuleScanner 一个扫描引擎

``threads``
--------------------

扫描线程数，默认值为 20 个。


``log_level``
--------------------

扫描任务的日志级别，其范围：info、debug、error。


``work_dir``
--------------------

扫描的工作目录，默认目录为: "/data/seecode/"。


``project_ssh``
--------------------

项目 git 地址，如: "git@github.com/seecode-audit/vuln_java.git" 或 "https://github.com/seecode-audit/vuln_java.git"。

``project_web``
--------------------

项目的 http 访问地址， 如: "https://github.com/seecode-audit/vuln_java"。


``project_name``
--------------------

项目名称，如: "vuln_java"。


``project_branch``
--------------------

分支名称，如: "master"。


``project_type``
--------------------

项目类型，其范围分为： online、offline。

  - online 为线上项目，其必须包含 project_ssh 参数，用于使用 git 来拉取源代码
  - offline 为线下项目，其必须包含 project_ssh 参数，用于下载压缩文件，系统默认只支持 zip 压缩


``project_storage_type``
-----------------------------

离线文件的存储方式，其范围: local, ftp, aws

  - local 代码文件在本地存储
  - ftp 需要使用 ftp 进行下载
  - aws 需要使用 aws 进行下载


``project_file_origin_name``
-------------------------------------

离线文件原始名称, 当 project_type 类型为 offline 时有效。


``project_file_hash``
------------------------

离线文件文件 MD5, 当 project_type 类型为 offline 时有效。



``group_name``
--------------------

项目分组名称，如: "线下项目组"。


``group_key``
--------------------

分组 key，如: "xianxiaxiangmuzu"。


``evidence_start_line_offset``
-------------------------------------

取证开始行偏移，默认为 -1，问题行的上一行。



``evidence_count``
--------------------

取证总行数，默认 5。


``force_sync_code``
--------------------

强制同步线上代码，布尔型参数，默认为 True。


``sync_vuln_to_server``
--------------------------

同步漏洞到 server 需要与 task_id 参数一起使用，布尔型参数，默认为 True。


``result_format``
--------------------
结果格式，默认 "json" 格式(目前只支持 json )。


``result_file``
--------------------
结果文件，默认为 task_id 作为结果的文件名称，如: "453.json"。
