

============
4 扫描结果
============

扫描结果目前只支持 json 格式，内容格式如下：

.. code-block:: json

    {
        "749c86838b5d24a64ed2b40fb18f5af4": {
            "rule_key": "java:apache-solr-cve-2019-0192",
            "risk_id": 3,
            "category": "vulnerability",
            "title": "Apache Solr \u8fdc\u7a0b\u4ee3\u7801\u6267\u884c(CVE-2019-0192)",
            "file": "pom.xml",
            "author": "MyKings",
            "author_email": "xsseroot@gmail.com",
            "hash": "d3f491ad09eaa9f7923edd2e041099e81171eb38",
            "start_line": 37,
            "end_line": 38,
            "report": "https://github.com/seecode-audit/vuln_java/blob/master/pom.xml#L37",
            "code_example": "            <artifactId>solr-solrj</artifactId>\n            <version>5.5.3</version>\n        </dependency>\n        <dependency>\n            <groupId>org.apache.shiro</groupId>\n",
            "is_false_positive": false,
            "whitelist_rule_id": "",
            "evidence_content": "5.5.3",
            "engine": 2
    }

4.1 参数说明
===============

``rule_key``
-----------------

检测规则的 key。

``risk_id``
-----------------

安全风险对应的ID

``category``
-----------------

风险类型，默认三种：Code Smell、Bug、Vulnerability（不区分大小写）。

``title``
-----------------

安全风险的标题。


``file``
-----------------

存在安全风险的文件路径，路径为绝对路径。

``author``
-----------------

文件最后的修改作者（必须为线上项目才会存在这个内容）。

``author_email``
----------------------

文件最后的修改作者邮箱（必须为线上项目才会存在这个内容）。

``hash``
-----------------

文件最后的 commit id（必须为线上项目才会存在这个内容）。

``start_line``
-----------------

问题存在的开始行。

``end_line``
-----------------

问题存在的结束行。

``report``
-----------------

  扫描的文件报告 URL。

  - 如果为 SonarScanner 引擎，报告地址为 SonarQube 中的文件地址。
  - 如果为线上项目，报告地址为 gitlab 或 github 的文件地址。

``code_example``
-----------------

取证的代码片段，默认为 6 行。

``evidence_content``
----------------------

取证匹配到的内容。

``is_false_positive``
----------------------

是否为误报。

``whitelist_rule_id``
----------------------

误报白名单检测的规则ID。

``engine``
-----------------

引擎类型，默认如下：

  - 1 代表 SonarScanner
  - 2 代表 RuleScanner
  - 3 代表 PluginScanner
