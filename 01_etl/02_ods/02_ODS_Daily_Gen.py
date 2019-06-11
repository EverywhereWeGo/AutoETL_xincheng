# -*- coding:utf-8 -*-
# !/usr/bin/python

import re
import xlrd
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def open_excel_0(excel_schema_name, excel_tab_name, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    src_tablename = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\0")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{fileds}", fileds)
    return output_str


def open_excel_1(excel_schema_name, excel_tab_name, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    src_tablename = ""
    keyid = ""
    oncondition = ""
    oncondition_template = "T1.{keyid} = T2.{keyid} AND "
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
            if (cols_info.cell_value(i, 8) == "Y"):
                keyid = cols_info.cell_value(i, 3)
                oncondition = oncondition + oncondition_template.replace("{keyid}", keyid)
    fileds = fileds.rstrip(",\n")
    oncondition = oncondition[:-4]
    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\1")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{oncondition}", oncondition). \
        replace("{keyid}", keyid). \
        replace("{fileds}", fileds)

    return output_str


def open_excel_2(excel_schema_name, excel_tab_name, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    fileds = ""
    SRC = ""
    src_tablename = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
    fileds = fileds.rstrip(",\n")

    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\2")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{src_tablename}", src_tablename). \
        replace("{fileds}", fileds)

    return output_str


def open_excel_3(excel_schema_name, excel_tab_name, src_system):
    cols_info = work_book.sheet_by_name("Col_Info_" + src_system)
    cols_nrows = cols_info.nrows

    fileds = "\n"
    SRC = ""
    src_tablename = ""
    keyid = ""
    SELECTKEYID = ""
    SELECTKEYIDwithalias = ""
    oncondition = ""
    oncondition_template = "T1.{keyid} = T2.{keyid} AND "
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 6).lower() == excel_tab_name.lower()):
            fileds = fileds + cols_info.cell_value(i, 3) + ",\n"
            SRC = cols_info.cell_value(i, 0)
            src_tablename = cols_info.cell_value(i, 1)
            if (cols_info.cell_value(i, 8) == "Y"):
                keyid = cols_info.cell_value(i, 3)
                SELECTKEYID = SELECTKEYID + keyid + ",\n"
                SELECTKEYIDwithalias = SELECTKEYIDwithalias + "T1." + keyid + ",\n"
                oncondition = oncondition + oncondition_template.replace("{keyid}", keyid)

    print SELECTKEYID
    fileds = fileds.rstrip(",\n")
    SELECTKEYID = SELECTKEYID.rstrip(",\n")
    SELECTKEYIDwithalias = SELECTKEYIDwithalias.rstrip(",\n")
    oncondition = oncondition[:-4]
    template_str = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\02_ods\daily\3")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ODSTABLE}", excel_tab_name). \
        replace("{SRC}", SRC). \
        replace("{SRCTABLE}", src_tablename). \
        replace("{KEYID}", keyid). \
        replace("{SELECTKEYID}", SELECTKEYID). \
        replace("{SELECTKEYIDwithalias}", SELECTKEYIDwithalias). \
        replace("{oncondition}", oncondition). \
        replace("{fileds}", fileds). \
        replace("{filedswithAliases}", fileds.replace("\n", "\nt2."))

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
        # 只获取前四列
        create_tab_list[i - 1] = [sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2),
                                  sheet.cell_value(i, 3)]
    return create_tab_list


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\ods.xlsx")
    des_file = r"C:\Users\Administrator\Desktop\GEN\DAILY\02ODS\%s\%s.hql"
    # all_system = ["ydac", "sy", "jjr", "my"]
    all_system = ["xcs"]
    for system in all_system:
        print system
        crt_tab_list_arr = get_create_tab_list(system)
        for i in range(0, len(crt_tab_list_arr)):
            all_str = ""
            filename = ""
            if (crt_tab_list_arr[i][3] == 0):
                all_str = open_excel_0(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1], system)
                filename = str(crt_tab_list_arr[i][1])
            elif (crt_tab_list_arr[i][3] == 1):
                all_str = open_excel_1(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1], system)
                filename = str(crt_tab_list_arr[i][1])
            elif (crt_tab_list_arr[i][3] == 2):
                all_str = open_excel_2(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1], system)
                filename = str(crt_tab_list_arr[i][1])
            elif (crt_tab_list_arr[i][3] == 3):
                all_str = open_excel_3(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1], system)
                filename = str(crt_tab_list_arr[i][1]) + "_all_day"

            des_file = r"C:\Users\Administrator\Desktop\GEN\DAILY\02ODS\%s\%s.hql" \
                       % (system, filename.lower())
            file_write = codecs.open(des_file, 'w', 'utf-8')
            file_write.writelines(all_str)