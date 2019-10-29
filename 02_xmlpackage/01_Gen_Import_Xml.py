# -*- coding:utf-8 -*-
# !/usr/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import uuid
import os
import codecs
import shutil
import zipfile


# 获取指定文件夹下所有脚本名称(带路径)
def get_filelist(pa):
    Filelist = []
    for home, dirs, files in os.walk(pa):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Filelist


def gen_job_xml(files, pa):
    xmls = ""
    for filenames in files:
        # 复制到目标文件夹一份
        shutil.copy(filenames, destination_folder)
        # 获取纯粹的脚本名
        filename = filenames[filenames.rindex(os.path.sep) + 1:]
        # 脚本的相对路径用于bdos中的层级显示
        pat = filenames[len(pa):filenames.rindex(os.path.sep)].replace(os.path.sep, "/")
        code = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(filename))).replace("-", '')

        type_code = ""
        # 根据文件类型判断种类
        if (filename.find(r".sh") != -1):
            type_code = "1"
        elif (filename.find(r".py") != -1):
            type_code = "2"
        elif (filename.find(r".hql") != -1):
            type_code = "3"

        xmls = xmls + """<file tree_name="%s" info_code="%s" type_code="%s" mr="0" queue="" priority="" remark="" path="%s"/>\n\t\t""" \
               % (filename, code, type_code, pat)
    return xmls


# 生成xml文件
def record_py_file(strin):
    project_path = "/Users/everywherewego/PycharmProjects/autoetl_xincheng"
    # 读取模板文件
    template_file = project_path + "/00_config/template/04_xml_import/xml_import"
    with open(template_file, 'r') as f:
        file_read = f.read()
    stri = file_read.replace("{0}", strin)

    file_name = "b82c2f2f309e4a4b962f858163dee4af.xml"
    des_file = destination_folder + os.path.sep + file_name
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(stri)
    file_write.close()


# 生成zip包
def gen_zip(zip_path):
    os.remove(zip_path)
    newZip = zipfile.ZipFile(zip_path, 'a')

    files = get_filelist(destination_folder)
    for filenames in files:
        shutil.copy(filenames, os.getcwd())

    files = get_filelist(os.getcwd())
    for filenames in files:
        #写入除了脚本名之外的文件到zip。为什么不从destination_folder文件夹直接复制，因为会连同父级路径结构一起打包，所有先移到脚本同一级路径
        if (filenames.replace(os.path.sep, "/") != sys.argv[0]):
            newZip.write(filenames.replace(os.getcwd() + os.path.sep, ""), compress_type=zipfile.ZIP_DEFLATED)
            os.remove(filenames)
    newZip.close()


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
    # 存放所有脚本的路径
    destination_folder = "/Users/everywherewego/Desktop/XML"
    # zip生成的路径
    zip_destination = "/Users/everywherewego/Desktop/xml.zip"
    # 所有生成的脚本的父文件夹
    script_path = "/Users/everywherewego/Desktop/GEN"
    # 清理工作，为了重跑
    del_file(destination_folder)
    scriptsname = get_filelist(script_path)
    xml_str = gen_job_xml(scriptsname, script_path)
    record_py_file(xml_str)
    gen_zip(zip_destination)
