
============
1 安装配置
============

1.1 安装
==============

环境初始化
------------


初始化系统环境与安装依赖，建议单独创建一个账号来运行扫描引擎。

.. code-block:: bash

  $ sudo yum install -y perl perl-Digest-MD5 unzip git


安装 python 3.6 环境

.. code-block:: bash

  $ sudo yum install -y centos-release-scl rh-python36 && scl enable rh-python36 bash
  $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
  $ echo "export PYTHONIOENCODING=utf-8" >> ~/.bashrc && source ~/.bashrc


sonarscanner 安装
---------------------

sonarscanner 官方下载地址： `https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/ <https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/>`_ ，
下载 sonarscanner 并解压到 /usr/local/ 目录下，为 sonarscanner 工具创建一个软链接到 /usr/bin/sonar-scanner。

.. code-block:: bash

  $ wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.0.0.1744-linux.zip
  $ sudo unzip sonar-scanner-cli-4.0.0.1744-linux.zip -d /usr/local/ && \
    ln -s /usr/local/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner /usr/bin/sonar-scanner

cloc 安装
---------------------

使用 yum 进行安装，如果 yum 不能安装可以手动下载安装：

.. code-block:: bash

  $ sudo yum install -y cloc


下载 cloc-1.82 安装：


.. code-block:: bash

  $ sudo wget https://github.com/AlDanial/cloc/releases/download/1.82/cloc-1.82.pl && \
    cp cloc-1.82.pl /usr/bin/cloc

账号配置
---------------------

创建 seecode 账号, 并设置密码：

.. code-block:: bash

  $ sudo useradd -m -s /bin/bash seecode && passwd seecode

登录 seecode 账户，创建 SSH 密钥对，得到 /home/seecode/.ssh/id_rsa 私钥；/home/seecode/.ssh/id_rsa.pub 公钥两个文件。

.. code-block:: bash

  $ su - seecode
  $ mkdir ~/.ssh && ssh-keygen



配置 gitlab 中 "个人资料" -> "SSH 密钥"， 将 id_rsa.pub 内容添加到配置中。

.. code-block:: bash

  $ cat /home/seecode/.ssh/id_rsa.pub


1.2 升级
==============

.. code-block:: bash

  $  seecode-scanner --upgrade
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

                 SeeCode Audit  seecode-scanner/1.0.0-20190903 xsseroot#gmail.com

  ---------------------------------------------------------------------------------------------------

  [15:18:36] [INFO] Check the latest version...
  [15:18:36] [INFO] [+] The server has opened the encrypted communication.
  [15:18:36] [INFO] The latest version of: [v1.85.14]
  [15:18:36] [INFO] Initialize the upgrade environment and create an upgrade directory...
  [15:18:36] [INFO] Start upgrading, check if the local version is consistent with the server version...
  [15:18:36] [INFO] current version: [v1.1.1], new version: [v1.85.14].
  [15:18:36] [INFO] Start downloading the upgrade package...
  [15:18:36] [INFO] Start decompressing the encryption upgrade package...
  [15:18:37] [INFO] Unzip the encryption upgrade package to complete.
  [15:18:37] [INFO] Start decompressing the decryption upgrade package...
  [15:18:37] [INFO] Decompression and decryption upgrade package completed
  [15:18:37] [INFO] Start syncing scan templates...
  [15:18:37] [INFO] Synchronous scan template completion.
  [15:18:37] [INFO] Start syncing whitelist plugin...
  [15:18:37] [INFO] Synchronous whitelist plugin completed.
  [15:18:37] [INFO] Start updating the current version to v1.85.14.
  [15:18:37] [INFO] Upgrade completed, current version: v1.85.14

1.3 采集
==============


1.4 检测配置
==============


.. code-block:: bash

  $  seecode-scanner -t
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
    
    [07:24:03] [INFO] [CORE] Start testing whether the core file of seecode-scanner exists...
    [07:24:03] [ERROR] [-] "/etc/seecode_scanner.yml" file not found.
    [07:24:03] [INFO] [+] Discover "/data/seecode/" directory.
    [07:24:03] [INFO] [SERVER] Start detecting service list files...
    [07:24:03] [ERROR] [-] "/usr/local/etc/seecode/conf/services.json" file not found.
    [07:24:03] [INFO] [SERVER] Start detecting core files...
    [07:24:03] [ERROR] [-] "monitor_url" is not set, the current content is: None.
    [07:24:03] [ERROR] [-] "upgrade_url" is not set, the current content is: None.
    [07:24:03] [ERROR] [-] "task_url" is not set, the current content is: None.
    [07:24:03] [INFO] [SCAN] Start testing whether the scan template of seecode-scanner exists...
    [07:24:03] [INFO] [+] Found "/seecode_scanner/profiles/normal.xml" file.
    [07:24:03] [INFO] [+] Found "/seecode_scanner/profiles/component_scan.xml" file.
    [07:24:03] [INFO] [+] Found "/seecode_scanner/profiles/default.xml" file.
    [07:24:03] [INFO] [ENGINE] Start detecting the scan engine...
    [07:24:03] [INFO] [+] Found the "sonar-scanner" tool with the path "/usr/bin/sonar-scanner"
    ========================================================================================================================
       NAME          ||    STATUS    ||    VERSION    ||           DESCRIPTION
    ========================================================================================================================
       Core          |    MISSING   |       -       |    -
    ------------------------------------------------------------------------------------------------------------------------
       Server        |    MISSING   |       -       |    -
    ------------------------------------------------------------------------------------------------------------------------
       Scan Template |    FOUND     |       -       | /seecode_scanner/profiles/normal.xml
       Scan Template |    FOUND     |       -       | /seecode_scanner/profiles/component_scan.xml
       Scan Template |    FOUND     |       -       | /seecode_scanner/profiles/default.xml
    ------------------------------------------------------------------------------------------------------------------------
       Engine        |    FOUND     |       -       | seecode_scanner.lib.engines.sonarscanner (/usr/bin/sonar-scanner)
       Engine        |    FOUND     |       -       | seecode_scanner.lib.engines.rulescanner
       Engine        |    FOUND     |       -       | seecode_scanner.lib.engines.pluginscanner
    ------------------------------------------------------------------------------------------------------------------------