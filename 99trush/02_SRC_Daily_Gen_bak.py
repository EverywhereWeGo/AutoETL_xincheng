# -*- coding:utf-8 -*-
# !/usr/bin/python

import time
import xlrd
import codecs

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

src_system = "my"


# 处理excel，生成执行语句
def open_excel(sheetname):
    # 读取sqoop的环境配置
    with open(r"C:\Users\Administrator\Desktop\AutoETL\00_config\sqoop_env_config", 'r') as f:
        sqoop_env = f.read()

    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name(sheetname)
    nrows_cfg = sh_cfg.nrows
    for i in range(1, nrows_cfg):
        srctype = ""
        srctablename = ""
        destablename = ""
        if (sh_cfg.cell_value(i, 0).lower() == "mysql"):
            srctype = "str_to_date('%s', '%%Y-%%m-%%d %%H')"
            srctablename = sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
        elif (sh_cfg.cell_value(i, 0).lower() == "oracle"):
            srctype = "to_date('%s', 'yyyy-mm-dd,hh24:mi:ss')"
            srctablename = sh_cfg.cell_value(i, 1) + "." + sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)
        elif (sh_cfg.cell_value(i, 0).lower() == "sql server"):
            srctype = "cast('%s' as datetime)"
            srctablename = sh_cfg.cell_value(i, 1) + "." + sh_cfg.cell_value(i, 2)
            destablename = sh_cfg.cell_value(i, 4) + "." + sh_cfg.cell_value(i, 5)

        sqoop_cmd = ""
        # 全量
        if (sh_cfg.cell_value(i, 6) == 1):
            password_ = """sqoop import  -D mapreduce.job.queuename=hadoop01 -D mapreduce.job.name={mjn} \\\n""" \
                        """--connect  '%s' \\\n""" \
                        """--username %s \\\n""" \
                        """--password '%s' \\#""" \
                        """--table '{srctablename}' \\\n""" \
                        """--hive-import \\\n""" \
                        """--hive-table {destablename} \\\n""" \
                        """--delete-target-dir \\\n""" \
                        """--hive-overwrite  -m 1 \\\n""" \
                        """--fetch-size 1000 \\\n""" \
                        """-- --schema '{schema}' \\\n""" \
                        """--null-string '' \\\n""" \
                        """--null-non-string '' \\\n""" \
                        """--hive-drop-import-delims \\\n""" \
                        """--fields-terminated-by '\\\\0x7F' \\\n""" \
                        """\"\"\"\\\n""" \
                        """%(connect,username,password)"""
            sqoop_template = password_
            sqoop_cmd = sqoop_template.replace("{mjn}", srctablename). \
                replace("{srctablename}", srctablename). \
                replace("{destablename}", destablename). \
                replace("{schema}", sh_cfg.cell_value(i, 1))

        # 增量
        elif (sh_cfg.cell_value(i, 6) == 0):
            sqoop_template = """sqoop import  -D mapreduce.job.queuename=hadoop01 -D mapreduce.job.name={mjn} \\\n""" \
                             """--connect  '%s' \\\n""" \
                             """--username %s \\\n""" \
                             """--password '%s' \\\n""" \
                             """--query "select * from {srctablename} where {condition} >= {srctype} AND \$CONDITIONS" \\\n""" \
                             """--target-dir 'sqoop-sql-import/wangchongnew.sql_{timestamp}' \\\n""" \
                             """--hive-import \\\n""" \
                             """--hive-table {destablename} \\\n""" \
                             """--delete-target-dir \\\n""" \
                             """--hive-overwrite -m 1 \\\n""" \
                             """--fetch-size 1000 \\\n""" \
                             """--null-string '' \\\n""" \
                             """--null-non-string '' \\\n""" \
                             """--hive-drop-import-delims \\\n""" \
                             """--fields-terminated-by '\\\\0x7F' \\\n""" \
                             """\"\"\"\\\n""" \
                             """%(connect,username,password,excute_date)"""
            sqoop_cmd = sqoop_template.replace("{mjn}", srctablename). \
                replace("{srctablename}", srctablename). \
                replace("{condition}", sh_cfg.cell_value(i, 7)). \
                replace("{timestamp}", str(int(round(time.time() * 1000)))). \
                replace("{destablename}", destablename). \
                replace("{srctype}", srctype)

        if (sh_cfg.cell_value(i, 0).lower() == "sql server"):
            sqoop_cmd1 = sqoop_cmd.replace("#", "\n--driver 'net.sourceforge.jtds.jdbc.Driver' \\\n")
        else:
            sqoop_cmd1 = sqoop_cmd.replace("#", "\\\n")
        print sqoop_cmd1
        record_py_file(sh_cfg.cell_value(i, 5).lower(), sqoop_env + sqoop_cmd1)


def record_py_file(file_name, sqoop):
    # 读取模板文件
    print sqoop
    template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\01_src\src_load_file"
    with open(template_file, 'r') as f:
        file_read = f.read()
    sqoop_cmd = file_read.replace("{section}", src_system).replace("{0}", sqoop)

    # 指定文件生成路径
    des_file = r"C:\Users\Administrator\Desktop\GEN\DAILY\01SRC\%s\%s.py" % (src_system, file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(sqoop_cmd)

    file_write.close()


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\src.xlsx")
    open_excel("load_cfg_" + src_system)
