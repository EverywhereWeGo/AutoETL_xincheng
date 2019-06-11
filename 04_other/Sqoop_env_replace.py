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
    sqoop_cmd = """
    new_str = """\
    sqoopenv = config.get('sqoopenv', 'sqoopenv')
    sqoop_cmd = """

    path = unicode(r"C:\Users\Administrator\Desktop\scriptExport_1559731758156", 'utf-8')
    for home, dirs, files in os.walk(path):
        for filename in files:
            stri = read_template_file(os.path.join(home, filename))
            res_str = stri.replace(old_str, new_str)
            print res_str

            des_file = r"C:\Users\Administrator\Desktop\new\%s" % (filename)
            file_write = codecs.open(des_file, 'w', 'utf-8')
            file_write.writelines(res_str)
            file_write.close()
