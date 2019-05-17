# -*- coding:utf-8 -*-
# !/usr/bin/python

import time
import xlrd
import codecs

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

src_system = "ydac"


# 处理excel，生成执行语句
def open_excel(sheetname):
    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name(sheetname)
    nrows_cfg = sh_cfg.nrows
    for i in range(1, nrows_cfg):
        srctypefunction = ""
        srctablename = ""
        destablename = ""
        if (sh_cfg.cell_value(i, 0).lower() == "mysql"):
            srctypefunction = "str_to_date('%s', '%%Y-%%m-%%d %%H')"
            srctablename = sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
        elif (sh_cfg.cell_value(i, 0).lower() == "oracle"):
            srctypefunction = "to_date('%s', 'yyyy-mm-dd,hh24:mi:ss')"
            srctablename = sh_cfg.cell_value(i, 1) + "." + sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
        elif (sh_cfg.cell_value(i, 0).lower() == "sql server"):
            srctypefunction = "cast('%s' as datetime)"
            srctablename = sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)

        sqoop_cmd = ""
        # 全量
        if (sh_cfg.cell_value(i, 6) == 1):
            template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\01_src\src_load_file_total"
            with open(template_file, 'r') as f:
                sqoop_template = f.read()

            sqoop_cmd = sqoop_template.replace("{section}", src_system).replace("{mjn}", srctablename). \
                replace("{srctablename}", srctablename). \
                replace("{destablename}", destablename). \
                replace("{schema}", sh_cfg.cell_value(i, 1))

        # 增量
        elif (sh_cfg.cell_value(i, 6) == 0):
            template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\01_src\src_load_file_incr"
            with open(template_file, 'r') as f:
                sqoop_template = f.read()

            sqoop_cmd = sqoop_template.replace("{section}", src_system).replace("{mjn}", srctablename). \
                replace("{srctablename}", srctablename). \
                replace("{condition}", sh_cfg.cell_value(i, 7)). \
                replace("{timestamp}", str(int(round(time.time() * 1000)))). \
                replace("{destablename}", destablename). \
                replace("{srctypefunction}", srctypefunction)

        if (sh_cfg.cell_value(i, 0).lower() == "sql server"):
            load_file = sqoop_cmd.replace("{--driver}\n", "--driver 'net.sourceforge.jtds.jdbc.Driver' \\\n")
        else:
            load_file = sqoop_cmd.replace("{--driver}\n", "")
        print load_file
        record_py_file(sh_cfg.cell_value(i, 5).lower(), load_file)


def record_py_file(file_name, load_file_str):
    # 指定文件生成路径
    des_file = r"C:\Users\Administrator\Desktop\GEN\DAILY\01SRC\%s\%s.py" % (src_system, file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(load_file_str)

    file_write.close()


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\src.xlsx")
    open_excel("load_cfg_" + src_system)
