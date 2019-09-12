
==============
2 Docker 部署
==============

使用 Docker 配置时，请先配置 seecode_scanner.yml 文件，配置说明请参考 `系统配置 <conf/core>`_ 。

2.1 创建镜像
===============


通过如下命令来创建一个 seecode-scanner 镜像，使用 docker images 来查看镜像是否创建成功。

.. code-block:: xml

  $ docker build -t seecode-scanner .


2.2 运行容器
===============


**创建容器是，请确保 seecode_scanner.yml 中配置的服务可用。**

以交互的方式创建一个 sca1 容器，并设置 shell 为 bash。

.. code-block:: xml

  $ docker run -it --name sca1 seecode-scanner /bin/bash


以后台服务方式创建一个 sca1 容器，默认启动 supervisord。

.. code-block:: xml

  $ docker run -d --name sca1 seecode-scanner

以交互的方式进入到 sca1 容器中。

.. code-block:: xml

  $ docker exec -it sca1 sh