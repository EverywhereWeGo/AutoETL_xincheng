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
        srctablename = ""
        destablename = ""
        dbfunction = ""
        arguments = ""
        if (sh_cfg.cell_value(i, 6) == 1):
            arguments = "(sqoopenv,onnect,username,password)"
            # 判断源数据库类型
            if (sh_cfg.cell_value(i, 0).lower() == "mysql"):
                dbfunction = " 1=1 "
                srctablename = sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
            elif (sh_cfg.cell_value(i, 0).lower() == "oracle"):
                dbfunction = " 1=1 "
                srctablename = sh_cfg.cell_value(i, 1) + "." + sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
            elif (sh_cfg.cell_value(i, 0).lower() == "sql server"):
                dbfunction = " 1=1 "
                srctablename = sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
        elif (sh_cfg.cell_value(i, 6) == 0):
            arguments = "(sqoopenv,connect,username,password,excute_date)"
            # 判断源数据库类型
            if (sh_cfg.cell_value(i, 0).lower() == "mysql"):
                dbfunction = " DATE(IFNULL({condition},'1999-01-01 00:00:00')) <= str_to_date('%s', '%%Y-%%m-%%d %%H')"
                srctablename = sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
            elif (sh_cfg.cell_value(i, 0).lower() == "oracle"):
                dbfunction = "nvl(to_date({condition}),date'1999-01-01') <= to_date('%s', 'yyyy-mm-dd,hh24:mi:ss')"
                srctablename = sh_cfg.cell_value(i, 1) + "." + sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
            elif (sh_cfg.cell_value(i, 0).lower() == "sql server"):
                dbfunction = "convert(varchar(10),ISNULL({condition}, '1999-01-01 00:00:00'),120) <= cast('%s' as datetime)"
                srctablename = sh_cfg.cell_value(i, 2)
                destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)

        # 判断字段是否需要特殊处理
        all_fileds = "*"
        if (sh_cfg.cell_value(i, 8).lower() == "y"):
            all_fileds = get_special_fileds(src_system, sh_cfg.cell_value(i, 2))

            print all_fileds

        # 读取增量模板
        template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\01_src\src_load_file_incr"
        with open(template_file, 'r') as f:
            sqoop_template = f.read()

        sqoop_cmd = sqoop_template.replace("{section}", src_system).replace("{mjn}", srctablename). \
            replace("{srctablename}", srctablename). \
            replace("{dbfunction}", dbfunction). \
            replace("{fileds}", all_fileds). \
            replace("{condition}", sh_cfg.cell_value(i, 7)). \
            replace("{timestamp}", str(int(round(time.time() * 1000)))). \
            replace("{destablename}", destablename). \
            replace("{arguments}", arguments)

        if (sh_cfg.cell_value(i, 0).lower() == "sql server"):
            load_file = sqoop_cmd.replace("{--driver}\n", "--driver 'net.sourceforge.jtds.jdbc.Driver' \\\n")
        else:
            load_file = sqoop_cmd.replace("{--driver}\n", "")
        # print load_file
        record_py_file(src_system, sh_cfg.cell_value(i, 5).lower(), load_file)


def get_special_fileds(src_system, tablename):
    cols_info = work_book.sheet_by_name("special_fileds_" + src_system)
    cols_nrows = cols_info.nrows
    fileds = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 2).lower() == tablename.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
    fileds = fileds.rstrip(",\n")
    # print fileds
    return fileds


def record_py_file(dirname, file_name, load_file_str):
    # 指定文件生成路径
    des_file = r"C:\Users\Administrator\Desktop\GEN\INIT\01SRC\%s\%s_init.py" % (dirname, file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    # print load_file_str
    file_write.writelines(load_file_str)

    file_write.close()


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\src.xlsx")
    all_system = ["my", "sy", "jjr", "ydac"]
    for i in all_system:
        open_excel("load_cfg_", i)
