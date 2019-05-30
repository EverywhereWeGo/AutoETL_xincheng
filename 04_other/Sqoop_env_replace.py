# -*- coding:utf-8 -*-
# !/usr/bin/python

import time
import xlrd
import codecs
import os

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def read_template_file(template_file):
    with open(template_file, 'r') as f:
        template_str = f.read()
    return template_str


if __name__ == '__main__':
    old_str = """\
export HADOOP_OPTS=" -DHADOOP_USER_NAME=wangchong"
export BDOS_SQOOP_HIVE_IP="manage-node1:2181,manage-node2:2181,manage-node3:2181"
export BDOS_SQOOP_HIVE_PORT=""
export BDOS_SQOOP_HIVE_NAMESPACE="test01"
export BDOS_SQOOP_HIVE_PARAM=";serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2"
export BDOS_SQOOP_HIVE_USERNAME="wangchong"
export BDOS_SQOOP_HIVE_PWD=""
"""
    new_str = """\
export HADOOP_OPTS=" -DHADOOP_USER_NAME=seazen"
export BDOS_SQOOP_HIVE_IP="sjzt-storagenode1:2181,sjzt-storagenode2:2181,sjzt-storagenode3:2181"
export BDOS_SQOOP_HIVE_PORT=""
export BDOS_SQOOP_HIVE_NAMESPACE="p1_property_src"
export BDOS_SQOOP_HIVE_PARAM=";serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2"
export BDOS_SQOOP_HIVE_USERNAME="seazen"
export BDOS_SQOOP_HIVE_PWD=""
"""

    path = unicode(r"C:\Users\Administrator\Desktop\scriptExport_1559198645459", 'utf-8')
    for home, dirs, files in os.walk(path):
        for filename in files:
            stri = read_template_file(os.path.join(home, filename))
            res_str = stri.replace(old_str, new_str)
            print res_str

            des_file = r"C:\Users\Administrator\Desktop\new\%s" % (filename)
            file_write = codecs.open(des_file, 'w', 'utf-8')
            file_write.writelines(res_str)
            file_write.close()
