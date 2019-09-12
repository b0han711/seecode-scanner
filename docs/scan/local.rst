

1 本地项目
=====================

扫描本地项目是根据现有的扫描规则模板对本地项目的代码安全检测，检测结果可保存为 json 文件，可供第三方系统调用使用。

下面是通过命令行方式对本地的 vuln_java 目录进行代码扫描，使用了默认 (default.xml) 的扫描模板。

.. code-block:: bash

    $ python cli.py --scan-path ./tmp/vuln_java --name vuln_java -o 1.json
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
    
    [02:36:13] [INFO] [ScanProject] Start syncing project code into the scan directory...
    [02:36:13] [INFO] [ScanProject] Synchronization project code completion.
    [02:36:13] [INFO] [ScanProject] Start executing exclusion rules...
    [02:36:13] [INFO] [ScanProject] Exclusion rule execution completed.
    [02:36:13] [INFO] [ScanProject] Start analyzing components...
    [02:36:13] [/opt/rh/rh-python36/root/usr/lib/python3.6/site-packages/clocwalk/cli.py(70)start()] [INFO] analysis statistics code ...
    [02:36:14] [INFO] [ScanProject] Project code line: [419], language: [Python], size: [116] KB
    [02:36:14] [INFO] [ScanProject] Start executing exclusion rules...
    [02:36:14] [INFO] [ScanProject] Exclusion rule execution completed.
    [02:36:14] [INFO] [RuleScanner] Begin to perform rule-based component vulnerability analysis...
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Apache Solr 远程代码执行(CVE-2019-0192)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Apache Shiro 反序列化漏洞 (RCE)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Spring Framework 远程代码执行(CVE-2018-1270)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'fastjson 远程代码执行漏洞' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 反序列化漏洞 (CVE-2019-12384)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 任意命令执行漏洞（CVE-2017-17485）' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind 反序列化漏洞（CVE-2017-7525）' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-12022)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-14719)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind polymorphic反序列化漏洞 (CVE-2018-19362)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Jackson-databind SubTypeValidator.java 存在远程代码执行漏洞 (CVE-2019-14379)' vulnerability.
    [02:36:14] [INFO] [RuleScanner] [Component] [+] Found 'Fastjson远程拒绝服务漏洞' vulnerability.
    [02:36:14] [INFO] [RuleScanner] Rule component scan completed.
    [02:36:14] [INFO] [RuleScanner] 正在执行黑名单检测...
    [02:36:14] [INFO] [RuleScanner] Begin to perform rule-based blacklist vulnerability analysis...
    [02:36:14] [INFO] [RuleScanner] Rule blacklist scan completed.
    [02:36:14] [INFO] [PluginScanner] 正在执行黑名单检测...
    [02:36:14] [INFO] [RuleScanner] 正在执行白名单过滤...
    [02:36:14] [INFO] [RuleScanner] False positive rule processing...
    [02:36:14] [INFO] [RuleScanner] Rule whitelist scan completed.
    [02:36:14] [INFO] [PluginScanner] 正在执行白名单过滤...
    [02:36:14] [INFO] [PluginScanner] False positive plugin processing...
    [02:36:14] [INFO] [PluginScanner] Plugin whitelist scan completed.
    [02:36:14] [INFO] [ScanProject] [+] Save the scan results to '/data/seecode/logs/vuln_java/1.json', total: 12.
    [02:36:14] [INFO] Analysis completed, time consuming: 1.57s
  
