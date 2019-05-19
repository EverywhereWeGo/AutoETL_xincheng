# -*- coding:utf-8 -*-
# !/usr/bin/python

import re
import xlrd
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def open_excel_0(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'

    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    fileds = ""
    ODS = ""
    ODSTABLE = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6) == excel_tab_name):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            ODS = cols_info.cell_value(i, 5)
            ODSTABLE = cols_info.cell_value(i, 6)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\0")
    output_str = template_str.replace("{ODS}", ODS). \
        replace("{ods_tablename}", ODSTABLE). \
        replace("{SRC}", "SRC"). \
        replace("{src_tablename}", excel_tab_name). \
        replace("{fileds}", fileds)
    return output_str


def open_excel_1(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'

    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    src_tablename = ""
    ODS = ""
    ODSTABLE = ""
    keyid = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6) == excel_tab_name):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
            ODS = cols_info.cell_value(i, 5)
            ODSTABLE = cols_info.cell_value(i, 6)
            if (cols_info.cell_value(i, 8) == "Y"):
                keyid = cols_info.cell_value(i, 3)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\1")
    output_str = template_str.replace("{ODS}", ODS). \
        replace("{ods_tablename}", ODSTABLE). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{keyid}", keyid). \
        replace("{fileds}", fileds)

    return output_str


def open_excel_2(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'
    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    ODS = ""
    ODSTABLE = ""
    src_tablename = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6) == excel_tab_name):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
            ODS = cols_info.cell_value(i, 5)
            ODSTABLE = cols_info.cell_value(i, 6)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\2")
    output_str = template_str.replace("{ODS}", ODS). \
        replace("{ods_tablename}", ODSTABLE). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{fileds}", fileds)

    return output_str


def open_excel_3(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'

    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    src_tablename = ""
    ODS = ""
    ODSTABLE = ""
    keyid = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6) == excel_tab_name):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
            ODS = cols_info.cell_value(i, 5)
            ODSTABLE = cols_info.cell_value(i, 6)
            if (cols_info.cell_value(i, 8) == "Y"):
                keyid = cols_info.cell_value(i, 3)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\3")
    output_str = template_str.replace("{ODS}", ODS). \
        replace("{ODSTABLE}", ODSTABLE). \
        replace("{SRC}", SRC). \
        replace("{SRCTABLE}", src_tablename). \
        replace("{KEYID}", keyid). \
        replace("{fileds}", fileds)

    return output_str


# 读取模板文件
def read_template_file(template_file):
    with open(template_file, 'r') as f:
        template_str = f.read()
    return template_str


# 获取"建表列表"sheet页
def get_create_tab_list():
    sheet = work_book.sheet_by_name("All_Table_Info")
    nrows_crt_tab = sheet.nrows
    ncols_crt_tab = sheet.ncols
    # 创建二维数组
    create_tab_list = [([0] * ncols_crt_tab) for i in range(nrows_crt_tab - 1)]
    # 从第二行开始遍历，因为第一行为属性注释
    for i in range(1, nrows_crt_tab):
        # 只获取前四列
        create_tab_list[i - 1] = [sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2),
                                  sheet.cell_value(i, 3)]
    return create_tab_list


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\ods_ydac.xlsx")
    crt_tab_list_arr = get_create_tab_list()
    for i in range(0, len(crt_tab_list_arr)):
        all_str = ""
        if (crt_tab_list_arr[i][3] == 0):
            all_str = open_excel_0(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])
        elif (crt_tab_list_arr[i][3] == 1):
            all_str = open_excel_1(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])
        elif (crt_tab_list_arr[i][3] == 2):
            all_str = open_excel_2(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])
        elif (crt_tab_list_arr[i][3] == 3):
            all_str = open_excel_3(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])

        des_file = r"C:\Users\Administrator\Desktop\GEN\DAILY\02ODS\%s.hql" % (crt_tab_list_arr[i][1].lower())
        file_write = codecs.open(des_file, 'w', 'utf-8')
        file_write.writelines(all_str)


