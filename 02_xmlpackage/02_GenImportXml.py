# -*- coding:utf-8 -*-
# !/usr/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import uuid
import os
import codecs
import shutil


# 获取指定文件夹下所有脚本名称
def get_filelist(pa):
    Filelist = []
    for home, dirs, files in os.walk(pa):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Filelist


def gen_job_xml(files, pa):
    xmls = ""
    for filenames in files:
        shutil.copy(filenames, "C:\Users\Administrator\Desktop\XML")
        filename = filenames[filenames.rindex("\\") + 1:]
        pat = filenames[len(pa):filenames.rindex("\\")].replace("\\", "/")
        code = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(filename))).replace("-", '')
        type_code = ""
        # 根据文件类型判断种类
        if (filename.find(r".sh") != -1):
            type_code = "1"
        elif (filename.find(r".py") != -1):
            type_code = "2"
        elif (filename.find(r".hql") != -1):
            type_code = "3"

        xmls = xmls + """<file tree_name="%s" info_code="%s" type_code="%s" mr="0" queue="" priority="" remark="" path="%s"/>\n      """ \
               % (filename, code, type_code, pat)
    return xmls


# 生成py文件
def record_py_file(strin):
    # 读取模板文件
    template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\xml_import"
    with open(template_file, 'r') as f:
        file_read = f.read()
    stri = file_read.replace("{0}", strin)

    file_name = "b82c2f2f309e4a4b962f858163dee4af.xml"
    des_file = r"C:\Users\Administrator\Desktop\XML\%s" % (file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(stri)
    file_write.close()


# 删除文件夹下所有文件
def del_file(del_path):
    ls = os.listdir(del_path)
    for i in ls:
        c_path = os.path.join(del_path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


# 主程序
if __name__ == '__main__':
    path = unicode("C:\Users\Administrator\Desktop\GEN", 'utf-8')

    del_file(r"C:\Users\Administrator\Desktop\XML")

    scriptsname = get_filelist(path)
    xml_str = gen_job_xml(scriptsname, path)
    record_py_file(xml_str)
