#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

from seecode_scanner import __version__


setup(
    name='seecode-scanner',
    version=__version__,
    description='seecode-scanner',
    author='MyKings',
    author_email='xsseroot@gmail.com',
    url='git@github.com:seecode-audit/seecode-scanner.git',
    packages=find_packages(),
    package_data = { '': [ '*.xml', '*.txt'] },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "seecode-scanner=seecode_scanner.cli:main"
        ]
    },
    install_requires=[
        'requests',
        'pyyaml',
        'func_timeout',
        'rsa',
        'gevent',
        'clocwalk>=0.2.0',
        'celery>=4.2.0',
        'redis',
        'requests',
    ],
    extras_require={
        'dev': [
            'devpi',
            'prospector',
            ],
        'test': [
            'coverage',
            'nose',
            ],
        'docs': [
            'Sphinx',
            'sphinx_rtd_theme',
            ],
        'build': [
            'devpi',
            ],
        },
    zip_safe=False,
)
