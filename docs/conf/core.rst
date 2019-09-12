
============
1 系统配置
============

1.1 Server
==============

该节点主要是 SeeCode Audit 服务端的相关配置信息，包括域名、认证Token、公钥路径、私钥路径。其配置内容如下：

.. code-block:: yaml

    server:
      domain: "http://seecode.com"
      api_uri: "/api/v2/"
      token: "dca58d563917b9325252f8a*********"
      public_key_path:
      private_key_path:

1.1.1 domain
------------

SeeCode Audit 服务端的域名，如：http://seecode.example.com。

1.1.2 api_uri
--------------------


SeeCode Audit 中 API 接口的 URI，默认为 /api/v2/

1.1.3 token
------------

SeeCode Audit 服务端的，认证 Token。


1.1.4 public_key_path
------------------------

与 SeeCode Audit 服务端通信使用人 RSA 公钥文件地址， 如：/home/seecode/public.pem。

1.1.5 private_key_path
------------------------

与 SeeCode Audit 服务端通信使用人 RSA 私钥文件地址，如：/home/seecode/private.pem。

----

1.2 Celery
==============

该节点是 Celery 配置信息，包括 border_url, timezone、c_force_root、task_timeout：

.. code-block:: yaml

    celery:
      broker_url: ""
      timezone: "Asia/Shanghai"
      c_force_root: False
      task_timeout: 7200

1.2.1 broker_url
--------------------

Celery Broker URL 地址，可以使用：Redis、RabbitMQR。

1.2.2 timezone
--------------------

Celery 中的时区，默认为："Asia/Shanghai"。

1.2.3 c_force_root
--------------------

Celery 的扫描任务是发运行使用 Root 账号运行， 默认为 False。

1.2.4 task_timeout
--------------------

Celery 的任务超时时间，单位为秒。默认 7200 秒。

----

1.3 HTTP
==============

该节点主要是 HTTP 相关参数设置，包括：超时时间、超时尝试、代理、请求头。

.. code-block:: yaml

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

1.3.1 timeout
------------------

访问 SeeCode Audit 服务端的超时等待的时间（requests.exceptions.Timeout） ，默认为 10 秒。

1.3.2 timeout_try
------------------

访问 SeeCode Audit 服务端超时后尝试重新尝试连接的次数，默认为 3 次。

1.3.3 failed_try
------------------

访问 SeeCode Audit 服务端发生失败（可以设置状态码）后尝试重新尝试连接的次数，默认为 3 次。

1.3.4 try_status_code
------------------------

设置失败的状态码（范围非200），默认为：500、502、503。

1.3.5 proxies
------------------

通过代理来访问 SeeCode Audit 服务。

http
^^^^^^^^^^^

http 协议的代理地址，如：http://192.168.1.1:8080

https
^^^^^^^^^^^

https 协议的代理地址，如：https://192.168.1.1:8080

socks5
^^^^^^^^^^^

socks5 协议的代理地址，如：socks5://192.168.1.1:8080

1.3.6 headers
---------------------

可以为 HTTP 中添加自定义请求头，如：accept-encoding、user-agent。

----

1.4 Distributed
==================

该节点是为了将扫描任务日志、扫描结果存储在一个公共存储区域。如：FTP、AWS。

.. code-block:: yaml

    distributed:
      ftp:
        host: "192.168.1.1"
        port: 21
        username: "seecode"
        password: "test1234"
        path: "/home/seecode/"


1.4.1 FTP
------------

host
^^^^^^^^^^^

FTP 服务的域名或者 IP 地址， 如：192.168.1.10。

port
^^^^^^^^^^^

FTP 服务的端口， 默认为 21。

username
^^^^^^^^^^^

FTP 服务的用户名，如：seecode。

password
^^^^^^^^^^^

FTP 用户的认证密码。

path
^^^^^^^^^^^

FTP 服务的存储路径，默认为：/home/seecode/。

1.4.2 AWS (TODO)
-------------------

该配置暂时未实现。