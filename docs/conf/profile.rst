
============
2 扫描模板
============

扫描模板主要是通过 SeeCode Audit 系统来自动生成，并通过 ``seecode-scanner --upgrade`` 命令进行升级，
您也可以手动编辑扫描模板来满足自己的扫描需求。


工具默认自带了：SonarScanner、RuleScanner、PluginScanner 三种扫描引擎。针对不同的扫描引擎有不同的参数设置，下面会逐一说明。


seecode-scanner 使用 xml 文件来编写扫描模板，其主要包含 config 与 engines 两个节点，描模板的内容大致如下：

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <template version="1.0.0">
        <config>
            <name>normal</name>
            <version>6.0</version>
            <exclude_dir>.git/,bin/,node_modules/,assets/,static/,.svn/</exclude_dir>
            <exclude_ext>.jpg,.jpeg,.png,.bmp,.gif,.ico,.cur,</exclude_ext>
            <exclude_file></exclude_file>
        </config>
        <engines>
            <engine></engine>
        </engines>
    </template>


2.1 template 根节点
====================

:属性:

``version``
--------------------

用于记录扫描模板格式内容的版本号，默认使用三位。


2.2 config 子节点
====================

``name``
--------------------

模板名称，命名规则建议使用小写英文字母或下划线。如系统自带的：default、normal、component_scan。

``version``
--------------------

模板的版本，用于区分同一个模板不同时间的配置，版本号使用浮点数默认保留一位小数，如：2.1。

``exclude_dir``
--------------------

扫描时不包含的路径，如：.git/,.svn/。多个路径使用英文逗号(,)分隔。

``exclude_ext``
--------------------

扫描时不包含的文件后缀，如：readme.md。多个路径使用英文逗号(,)分隔。

``exclude_file``
--------------------

扫描时不包含的文件，如：.log,.txt。多个路径使用英文逗号(,)分隔。

2.3 engine 子节点
====================

engine 是 engines 下的子节点，engines 必须包含一个或多个 engine 节点。

:属性:

``name``
--------------------

扫描引擎名称，默认包含三个引擎，名称分别为：SonarScanner、RuleScanner、PluginScanner。

:节点:

``parameters``
--------------------


扫描引擎的全局参数设定如下, 这里用了 SonarScanner 引擎的全局参数进行说明：

.. _扫描引擎全局参数 :

.. code-block:: xml

    <parameters>
          <!-- SonarQube 服务端的认证 Token -->
          <item name="API_TOKEN">80828d9343317970f*********</item>

          <!-- SonarQube 服务端的 API 地址 -->
          <item name="API_DOMAIN">http://sonar7.example.com</item>

          <!-- sonar-scanner 工具路径 -->
          <item name="SONAR_SCANNER_PATH">/usr/bin/sonar-scanner</item>

          <!-- SonarScanner 引擎的执行超时时间，单位秒 -->
          <item name="ENGINE_TIMEOUT">1200</item>

          <!-- SonarScanner 连接 SonarQube 服务端的超时时间，单位秒 -->
          <item name="HTTP_TIMEOUT">10</item>

          <!-- SonarScanner 连接 SonarQube 服务端的超时尝试次数 -->
          <item name="HTTP_TIMEOUT_RETRY">3</item>

          <!-- SonarScanner 连接 SonarQube 服务端的非超时失败尝试次数 -->
          <item name="HTTP_FAILED_RETRY">3</item>

          <!-- sonar 扫描的配置文件, 全局参数参数
          {{project_key}}： 项目的key
          {{project_name}}：项目名称
          {{sonar_host}}：sonarqube 地址，使用 API_DOMAIN 替换
          {{sonar_login}}：sonarqube token，使用 API_TOKEN 替换
          -->
          <item name="SONAR_PROJECT_PROPERTIES">sonar.projectKey={{project_key}}&#13;
                    sonar.projectName={{project_name}}&#13;
                    sonar.projectVersion=1.0&#13;
                    sonar.sources=.&#13;
                    sonar.sourceEncoding=UTF-8&#13;
                    sonar.exclusions=**/node_modules/**/*.*,&#13;
                    sonar.host.url={{sonar_host}}&#13;
                    sonar.login={{sonar_login}}&#13;
                    sonar.java.binaries=.
          </item>
    </parameters>

**item**

* name

  - [属性]参数名称，建议使用大写字母。

* item 内容

  - 参数值。

----

``component``
--------------------

用于组件漏洞检测的扫描规则，默认只支持 RuleScanner，其中 SonarScanner、PuginScanner 引擎没有实现组件规则检测。


**RuleScanner 引擎**

.. code-block:: xml

    <component>
        <item id="7582">
            <name>Apache Solr 远程代码执行(CVE-2019-0192)</name>
            <key>java:apache-solr-cve-2019-0192</key>
            <revision>0.43</revision>
            <risk id="3">中危</risk>
            <category>Vulnerability</category>
            <match_type>name</match_type>
            <match_content><![CDATA[solr-solrj]]></match_content>
            <match_regex flag="I"><![CDATA[(5\.[0-5]{1}) ### 5.0-5.5
		(5\.2\.1) ### 5.0-5.5
		(5\.3\.[1-2]{1}) ### 5.3.1 - 5.3.2
		(5\.4\.1) ### 5.4.1
		(5\.5\.[1-5]{1}) ### 5.5.1 - 5.5.5
		(6\.[0-6]{1})
		(6\.0\.1)
		(6\.1\.1)
		(6\.2\.1)
		(6\.4\.[1-2]{1})
		(6\.5\.1)
		(6\.6\.[1-5]{1})]]>
            </match_regex>
        </item>
    </component>

**item**

.. _component中id :

* id

  - [属性]为整数型，默认为 SeeCode Audit 中的规则 ID。

.. _component中name :

* name

  - 规则名称，如：`Apache Solr 远程代码执行(CVE-2019-0192)`。

.. _component中key :

* key

  - 规则 Key 使用小写的英文字母，其主要有两部分组成，并使用英文的冒号(:)分割，第一部分代表组件使用的语言，第二部分代表组件相关信息。

.. _component中revision :

* revision

  - 规则修订的版本号，默认使用浮点型并保留两位小数。

.. _component中risk :

* risk

  - id 是在 SeeCode Audit 中对应的编号，其为 risk 节点的一个属性。
  - 内容为风险描述，其范围为：严重、高危、中危、低危、信息五个级别。

.. _component中category:

* category

  - 规则所属类型，分为三种：Code Smell、Bug、Vulnerability，对应 sonarqube 中的类型（不区分大小写）。

.. _component中match_type:

* match_type

  - 匹配类分为两种，分别为：name、groupId。

.. _component中match_content:

* match_content

  - 匹配内容用于匹配组件的名称，必须是字符中格式，区分大小写。

.. _component中match_regex:

* match_regex

  - 匹配组件版本的正则表达式。
  - flag 用于正则的标志位，可选范围：I(忽略大小写)、M(多行匹配)、I|M(忽略大小写、多行匹配)。


----

``blacklist``
--------------------

黑名单是定义扫描规则用于发现漏洞或者安全风险。SonarScanner 引擎比较特殊，它不能设置任何(组件、黑名单、白名单)规则，如若需要定制扫描参数必须修改 扫描引擎全局参数_ 中的
SONAR_PROJECT_PROPERTIES 。

**(1) RuleScanner 引擎**

.. code-block:: xml

    <blacklist>
        <item id="7583">
            <name>密码硬编码</name>
            <key>common:password-hard</key>
            <revision>0.27</revision>
            <risk id="3">中危</risk>
            <category>Vulnerability</category>
            <match_type>content</match_type>
            <file_ext>.java</file_ext>
            <match_regex flag="I"><![CDATA[PARAM_NAME_password\s+=\s+['"].+['"]]]></match_regex>
        </item>
    </blacklist>


**item**

* id `略` ，同上 component中id_
* name `略` ，同上 component中name_
* key `略` ，同上 component中key_
* revision `略` ，同上 component中revision_
* risk `略` ，同上 component中risk_
* category `略`，同上 component中category_

* match_type

  - 匹配类分为三种，分别是：dir、file、content。

* file_ext ※

  - 该节点必须当 match_type 内容为 content 时才会出现, 多个文件后缀需要使用英文的逗号(,)分隔, 如：.java,.jsp。

* match_regex

  - ↑ 同上 component中match_regex_。


**(2) PluginScanner 引擎**

.. code-block:: xml

    <blacklist>
        <item id="7583">
            <name>反射型XSS检测</name>
            <key>java:reflective-xss</key>
            <revision>0.03</revision>
            <risk id="4">低危</risk>
            <category id="3">Vulnerability</category>
            <module>seecode_scanner.plugins.blacklist.reflective_xss_java</module>
            <script>plugins/whitelist/reflective_xss_java.py</script>
        </item>
    </blacklist>


**item**

* id `略`
* name `略`
* key `略`
* revision `略`
* risk `略`
* category `略`

* module

  - 插件所在的 seecode_scanner 的所在引用位置。

* script

  - 插件的 py 脚本文件路径，路径为相对路径。

----

``whitelist``
--------------------

白名单检测规则用于已经识别出的安全分析，进行的二次分析，主要用于减少误报。

**(1) RuleScanner 引擎**

.. code-block:: xml

    <whitelist>
        <item id="7580">
            <name>误报密码参数排除规则</name>
            <key>common:password-exclude</key>
            <revision>0.27</revision>
            <risk id="4">信息</risk>
            <category>BUG</category>
            <match_type>content</match_type>
            <match_regex flag=""><![CDATA[PARAM_NAME_PASSWORD\s+=\s+['"].+['"]]]></match_regex>
        </item>
    </whitelist>

**item**

* id `略` ，同上 component中id_
* name `略` ，同上 component中name_
* key `略` ，同上 component中key_
* revision `略` ，同上 component中revision_
* risk `略` ，同上 component中risk_
* category `略`，同上 component中category_

* match_type

  - 匹配类分为三种，分别是：dir、file、content。

* file_ext ※

  - 该节点必须当 match_type 内容为 content 时才会出现, 多个文件后缀需要使用英文的逗号(,)分隔, 如：.java,.jsp。

* match_regex

  - ↑ 同上 component中match_regex_。


**(2)PluginScanner 引擎**

.. code-block:: xml

    <whitelist>
        <item id="7583">
            <name>跳过测试文件与目录</name>
            <key>java:pass-test-file-dir</key>
            <revision>0.03</revision>
            <risk id="5">信息</risk>
            <category id="3">Vulnerability</category>
            <module>seecode_scanner.plugins.whitelist.pass_file_dir</module>
            <script>plugins/whitelist/pass_file_dir.py</script>
        </item>
    </whitelist>


**item**

* id `略`
* name `略`
* key `略`
* revision `略`
* risk `略`
* category `略`

* module

  - 插件所在的 seecode_scanner 的所在引用位置。

* script

  - 插件的 py 脚本文件路径，路径为相对路径。

