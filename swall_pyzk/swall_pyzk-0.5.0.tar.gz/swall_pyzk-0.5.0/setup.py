#!/usr/bin/env python
#coding:utf-8
__author__ = 'lufeng118@outlook.com'

import os
import sys
from setuptools import setup, Extension
from distutils.command.build import build
from subprocess import call
from multiprocessing import cpu_count

BASEPATH = os.path.dirname(os.path.abspath(__file__))
ZK_PATH = os.path.join(BASEPATH, 'c')
if not os.path.exists("/usr/local/lib/libzookeeper_mt.so.2.0.0"):
    call(["bash","configure"], cwd=ZK_PATH)
    call(["make","install"], cwd=ZK_PATH)
    os.system("echo '/usr/local/lib/' > /etc/ld.so.conf.d/zk_lib.conf")
    call(["ldconfig"], cwd=ZK_PATH)

zookeepermodule = Extension("zookeeper",
                            sources=["zookeeper.c"],
                            include_dirs=["/usr/include/c-client-src", "/usr/local/include/c-client-src",
                                    "/usr/include/zookeeper", "/usr/local/include/zookeeper"],
                            libraries=["zookeeper_mt"],
                            )

setup(
    name='swall_pyzk',
    version='0.5.0',
    description='swall_pyzk is a pylib of zookeeper for swall',
    maintainer='lufeng4828',
    maintainer_email='lufeng118@outlook.com',
    license='GPLv2',
    url='https://github.com/lufeng4828/swall.git',
    ext_modules=[zookeepermodule] 
)
