# -*- coding:utf-8 -*-
# !/usr/bin/python

import time
import xlrd
import codecs

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 处理excel，生成执行语句
def open_excel(sheetname, src_system):
    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name(sheetname + src_system)
    nrows_cfg = sh_cfg.nrows
    for i in range(1, nrows_cfg):
        # 判断源数据库类型
        schema = sh_cfg.cell_value(i, 1).lower()
        srctablename = sh_cfg.cell_value(i, 2)
        desdatabase = sh_cfg.cell_value(i, 4)
        destablename = sh_cfg.cell_value(i, 5)

        # 判断字段是否需要特殊处理
        all_fileds = "*"
        if (sh_cfg.cell_value(i, 8).lower() == "y"):
            all_fileds = get_special_fileds(src_system, sh_cfg.cell_value(i, 2))

        template_file = projectpath + "/autoetl_xincheng/00_config/template/01_src/increment"
        with open(template_file, 'r') as f:
            sqoop_template = f.read()

        sqoop_cmd = ""
        # 全量
        if (sh_cfg.cell_value(i, 6) == 1):
            pass
        # 增量
        elif (sh_cfg.cell_value(i, 6) == 0):
            incrementfiled = sh_cfg.cell_value(i, 7)

            sqoop_cmd = sqoop_template.replace("{mapjobname}", schema + "-" + srctablename + "-" + str(time.time())). \
                replace("{desdatabase}", desdatabase). \
                replace("{destablename}", destablename). \
                replace("{schema}", schema). \
                replace("{srctablename}", srctablename). \
                replace("{incrementfiled}", incrementfiled)

        record_py_file(src_system, (schema + "_" + srctablename).lower(), sqoop_cmd)


def get_special_fileds(src_system, tablename):
    cols_info = work_book.sheet_by_name("special_fileds_" + src_system)
    cols_nrows = cols_info.nrows
    fileds = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 2).lower() == tablename.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ","
    fileds = fileds.rstrip(",")
    return fileds


def record_py_file(dirname, file_name, load_file_str):
    # 指定文件生成路径
    des_file = r"/Users/everywherewego/Desktop/GEN/01stage/02daily/%s/%s.py" % (dirname, file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(load_file_str)

    file_write.close()


if __name__ == '__main__':
    projectpath = "/Users/everywherewego/PycharmProjects";
    # work_book = xlrd.open_workbook(projectpath + "/autoetl_xincheng/00_config/xlsx/src.xlsx")
    work_book = xlrd.open_workbook("/Users/everywherewego/Desktop/src_dm.xlsx")
    all_system = ["dm"]
    for i in all_system:
        open_excel("load_cfg_", i)
