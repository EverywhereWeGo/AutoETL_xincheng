# -*- coding:utf-8 -*-
# !/usr/bin/python

import time
import xlrd
import codecs


# 处理excel，生成执行语句
def open_excel():
    # 读取sqoop的环境配置
    with open(r"C:\Users\Administrator\Desktop\AutoETL\00_config\sqoop_env_config", 'r') as f:
        sqoop_env = f.read()

    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name("load_cfg")
    nrows_cfg = sh_cfg.nrows
    for i in range(1, nrows_cfg):
        if (sh_cfg.cell_value(i, 4) == 1):
            sqoop_template = """sqoop import  -D mapreduce.job.queuename=hadoop01 -D mapreduce.job.name={mjn} \\\n""" \
                             """--connect  '%%s' \\\n""" \
                             """--username %%s \\\n""" \
                             """--password '%%s' \\\n""" \
                             """--table '{srctablename}' \\\n""" \
                             """--hive-import \\\n""" \
                             """--hive-table {destablename} \\\n""" \
                             """--delete-target-dir \\\n""" \
                             """--hive-overwrite  -m 1 \\\n""" \
                             """--fetch-size 1000 \\\n""" \
                             """-- --schema 'JUPITER'""" \
                             """\"\"\"""" \
                             """%%(connect,username,password)"""
            sqoop_cmd = sqoop_template.replace("{mjn}", sh_cfg.cell_value(i, 3)). \
                replace("{srctablename}", sh_cfg.cell_value(i, 1)). \
                replace("{destablename}", sh_cfg.cell_value(i, 3))
            record_py_file(sh_cfg.cell_value(i, 3).replace(".", "_").lower() + "_totl", sqoop_env + sqoop_cmd)

        elif (sh_cfg.cell_value(i, 4) == 0):
            sqoop_template = """sqoop import  -D mapreduce.job.queuename=hadoop01 -D mapreduce.job.name={mjn} \\\n""" \
                             """--connect  '%%s' \\\n""" \
                             """--username %%s \\\n""" \
                             """--password '%%s' \\\n""" \
                             """--query "select * from {srctablename} where {contion} > to_date('%%s','yyyy-mm-dd,hh24:mi:ss') AND \$CONDITIONS" \\\n""" \
                             """--target-dir 'sqoop-sql-import/wangchongnew.sql_{timestamp}' \\\n""" \
                             """--hive-import \\\n""" \
                             """--hive-table {destablename} \\\n""" \
                             """--delete-target-dir \\\n""" \
                             """--hive-overwrite -m 1 \\\n""" \
                             """--fetch-size 1000 \\\n""" \
                             """\"\"\"""" \
                             """%%(connect,username,password,excute_date)"""
            sqoop_cmd = sqoop_template.replace("{mjn}", sh_cfg.cell_value(i, 1)). \
                replace("{srctablename}", sh_cfg.cell_value(i, 1)). \
                replace("{contion}", sh_cfg.cell_value(i, 5)). \
                replace("{timestamp}", str(int(round(time.time() * 1000)))). \
                replace("{destablename}", sh_cfg.cell_value(i, 3))

            record_py_file(sh_cfg.cell_value(i, 3).replace(".", "_").lower() + "_incr", sqoop_env + sqoop_cmd)


# 生成py文件
def record_py_file(file_name, sqoop_cmd):
    print sqoop_cmd
    # 读取模板文件
    template_file = r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\src_load_file"
    file_read = codecs.open(template_file, 'r', 'utf-8')
    # 指定文件生成路径
    des_file = r"C:\Users\Administrator\Desktop\DAILY\SRC\%s.py" % (file_name)
    file_write = codecs.open(des_file, 'w', 'utf-8')
    while (1):
        line = file_read.readline()
        if line:
            if (line.find("{0}") != -1):
                file_write.writelines(line.replace("{0}", sqoop_cmd))
            else:
                file_write.writelines(line)
        else:
            break
    file_read.close()
    file_write.close()


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\src.xlsx")
    open_excel()
