.. SeeCode Scanner documentation master file, created by
   sphinx-quickstart on Mon Sep  2 17:33:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SeeCode Scanner's documentation!
===========================================

.. contents:: Table of Contents
   :local:


What Is This?
---------------------------
.. include:: ../README.rst
  :start-after: rtd-inclusion-marker-do-not-remove

.. toctree::
   :caption: 配置
   :maxdepth: 2

   conf/core
   conf/profile
   conf/project
   conf/result


.. toctree::
   :caption: 部署
   :maxdepth: 2

   deploy/install
   deploy/docker

.. toctree::
   :caption: 使用
   :maxdepth: 2

   scan/local
   scan/online

.. toctree::
   :caption: 其他
   :maxdepth: 3

   changelog
   SeeCode Audit 使用手册 <https://github.com/seecode-audit/seecode-audit/wiki/>