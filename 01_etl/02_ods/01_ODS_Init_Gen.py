# -*- coding:utf-8 -*-
# !/usr/bin/python

import re
import xlrd
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def init_ods_with_partiton(excel_schema_name, excel_tab_name, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    select_str = ""
    date_flag = ""
    SRC = ""
    src_tablename = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            select_str = select_str + cols_info.cell_value(i, 3) + ",\n"
            if (cols_info.cell_value(i, 9) == "Y"):
                date_flag = cols_info.cell_value(i, 3)
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)

    select_str = select_str.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\init\ods_init_with_partitions")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{fileds}", select_str). \
        replace("{dateflag}", date_flag)

    return output_str


def init_ods_without_partition(excel_schema_name, excel_tab_name, templatenum, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    SRC = ""
    src_tablename = ""
    select_str = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            select_str = select_str + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
    select_str = select_str.rstrip(",\n")

    if (templatenum == 3):
        con_str = "p1_property_ods.data_check(%s) as con_str" % (select_str)
        select_str = select_str + ",\n" + con_str
        print select_str

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\init\ods_init_without_partition")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{fileds}", select_str)

    return output_str


# 读取模板文件
def read_template_file(template_file):
    with open(template_file, 'r') as f:
        template_str = f.read()
    return template_str


# 获取"建表列表"sheet页
def get_create_tab_list(src_system):
    sheet = work_book.sheet_by_name("Table_Info_" + src_system)
    nrows_crt_tab = sheet.nrows
    ncols_crt_tab = sheet.ncols
    # 创建二维数组
    create_tab_list = [([0] * ncols_crt_tab) for i in range(nrows_crt_tab - 1)]
    # 从第二行开始遍历，因为第一行为属性注释
    for i in range(1, nrows_crt_tab):
        create_tab_list[i - 1] = [sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2),
                                  sheet.cell_value(i, 3)]
    return create_tab_list


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\ods.xlsx")
    # all_system = ["ydac", "sy", "jjr", "my"]
    all_system = ["xcs"]
    for system in all_system:
        crt_tab_list_arr = get_create_tab_list(system)
        all_str = ""
        for i in range(0, len(crt_tab_list_arr)):
            if (crt_tab_list_arr[i][2] == "Y"):
                all_str = init_ods_with_partiton(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1], system)
            elif (crt_tab_list_arr[i][2] == "N"):
                all_str = init_ods_without_partition(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1],
                                                     crt_tab_list_arr[i][3], system)

            des_file = r"C:\Users\Administrator\Desktop\GEN\INIT\02ODS\%s\%s_init.hql" \
                       % (system, crt_tab_list_arr[i][1].lower())
            file_write = codecs.open(des_file, 'w', 'utf-8')
            file_write.writelines(all_str)
