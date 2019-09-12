

2 线上项目
=====================

线上扫描项目其大致流程是，通过 gitlab/github 等代码托管系统，来实时拉取线上代码进行扫描。 这是使用了 -c 参数，通过配置文件进行代码检测。

.. code-block:: bash
  
  $ python cli.py -c vuln_java.yaml
  ---------------------------------------------------------------------------------------------------
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
  
                   SeeCode Audit  seecode-scanner/1.0.0-20190911 xsseroot#gmail.com
  
  ---------------------------------------------------------------------------------------------------

  [02:52:18] [WARNING] [TaskStatus] Query scan task information failed, returned '404 - Not Found' when accessing [http://seecode.com/api/v2/task/9527/] API interface.
  [02:52:18] [INFO] [ScanProject] Start syncing project code into the scan directory...
  [02:52:18] [INFO] [GitOperator] Force update of local code...
  [02:52:22] [INFO] [GitOperator] Code synchronization completed.
  [02:52:22] [INFO] [ScanProject] current branch commit:d3f491ad09eaa9f7923edd2e041099e81171eb38, branch name:master
  [02:52:22] [INFO] [ScanProject] Synchronization project code completion.
  [02:52:22] [INFO] [ScanProject] Start executing exclusion rules...
  [02:52:22] [INFO] [ScanProject] Exclusion rule execution completed.
  [02:52:22] [INFO] [ScanProject] Start analyzing components...
  [02:52:22] [/opt/rh/rh-python36/root/usr/lib/python3.6/site-packages/clocwalk/cli.py(70)start()] [INFO] analysis statistics code ...
  [02:52:22] [INFO] [ScanProject] Project code line: [419], language: [Python], size: [124] KB
  [02:52:22] [INFO] [ScanProject] Start executing exclusion rules...
  [02:52:23] [INFO] [ScanProject] Exclusion rule execution completed.
  [02:52:23] [INFO] [RuleScanner] Begin to perform rule-based component vulnerability analysis...
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Apache Solr 远程代码执行(CVE-2019-0192)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Apache Shiro 反序列化漏洞 (RCE)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Spring Framework 远程代码执行(CVE-2018-1270)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'fastjson 远程代码执行漏洞' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 反序列化漏洞 (CVE-2019-12384)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 任意命令执行漏洞（CVE-2017-17485）' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 反序列化漏洞（CVE-2017-7525）' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-12022)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-14719)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-19362)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind SubTypeValidator.java 存在远程代码执行漏洞 (CVE-2019-14379)' vulnerability.
  [02:52:23] [INFO] [RuleScanner] [Component] [+] Found 'Fastjson远程拒绝服务漏洞' vulnerability.
  [02:52:23] [INFO] [RuleScanner] Rule component scan completed.
  [02:52:23] [INFO] [RuleScanner] 正在执行黑名单检测...
  [02:52:23] [INFO] [RuleScanner] Begin to perform rule-based blacklist vulnerability analysis...
  [02:52:23] [INFO] [RuleScanner] Rule blacklist scan completed.
  [02:52:23] [INFO] [RuleScanner] 正在执行白名单过滤...
  [02:52:23] [INFO] [RuleScanner] False positive rule processing...
  [02:52:23] [INFO] [RuleScanner] Rule whitelist scan completed.
  [02:52:23] [INFO] [ScanProject] [+] Save the scan results to '/data/seecode/logs/9527/9527.json', total: 12.
  [02:52:23] [INFO] Analysis completed, time consuming: 5.59s


vuln_java.yaml 文件的格式如下，具体配置文件的参数说明请参考 `项目配置 <conf/project>`_


.. code-block:: yaml
  
  scan:
    task_id: 9527
    template: "component_scan"
    threads: 20
    log_level: "info"
    work_dir: "/data/seecode/"
    project_ssh: "https://github.com/seecode-audit/vuln_java.git"
    project_web: "https://github.com/seecode-audit/vuln_java"
    project_name: "vuln_java"
    project_branch: "master"
    project_type: "online"
    project_storage_type: "local"
    project_file_origin_name: ""
    project_file_hash: ""
    group_name: "seecode-audit"
    group_key: "seecode-audit"
    evidence_start_line_offset: -1
    evidence_count: 5
    force_sync_code: True
    sync_vuln_to_server: False
    result_format: "json"
    result_file: "9527.json"