# -*- coding:utf-8 -*-
# !/usr/bin/python

import re
import xlrd
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def open_excel(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'

    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    select_str = ""
    keyid = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 2) == excel_tab_name):
            select_str = select_str + cols_info.cell_value(i, 11) + ",\n"
            if (cols_info.cell_value(i, 12) == "Y"):
                keyid = cols_info.cell_value(i, 11)

    template_str = read_template_file(r"C:\Users\Administrator\Desktop\autoload\00_config\scripttemplate\withouttimesstrample")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", "SRC"). \
        replace("{src_tablename}", excel_tab_name). \
        replace("{keyid}", keyid). \
        replace("{fileds}", select_str.rstrip("\n"))

    print output_str
    return output_str

def open_excel_with(excel_schema_name, excel_tab_name):
    sheet_name_col = excel_schema_name + '_col_lvl'
    cols_info = work_book.sheet_by_name(sheet_name_col)
    cols_nrows = cols_info.nrows

    select_str = ""
    for i in range(0, cols_nrows):
        if (cols_info.cell_value(i, 2) == excel_tab_name):
            select_str = select_str + cols_info.cell_value(i, 11) + ",\n"

    template_str = read_template_file(r"C:\Users\Administrator\Desktop\autoload\00_config\scripttemplate\withtimestarmper")
    output_str = template_str.replace("{ODS}", excel_schema_name). \
        replace("{ods_tablename}", excel_tab_name). \
        replace("{SRC}", "SRC"). \
        replace("{src_tablename}", excel_tab_name). \
        replace("{fileds}", select_str.rstrip("\n"))

    print output_str
    return output_str


# 获取"建表列表"sheet页
def get_create_tab_list():
    sheet = work_book.sheet_by_name("建表列表")
    nrows_crt_tab = sheet.nrows
    ncols_crt_tab = sheet.ncols
    print ncols_crt_tab
    print ([0] * ncols_crt_tab)
    # 创建二维数组
    create_tab_list = [([0] * ncols_crt_tab) for i in range(nrows_crt_tab - 1)]
    print create_tab_list
    # 从第二行开始遍历，因为第一行为属性注释
    for i in range(1, nrows_crt_tab):
        # 只获取前三列
        create_tab_list[i - 1] = [sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2)]
    return create_tab_list


# 读取模板文件
def read_template_file(template_file):
    template_str = ""
    file_read = codecs.open(template_file, 'r', 'utf-8')
    while (1):
        line = file_read.readline()
        if line:
            template_str = template_str + line
        else:
            break
    file_read.close()
    return template_str


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\autoload\00_config\xlsx\ods.xlsx")
    crt_tab_list_arr = get_create_tab_list()
    print crt_tab_list_arr
    for i in range(0, len(crt_tab_list_arr)):
        # 判断当列是否为空，如为空跨过
        pattern = re.compile(r'\w')
        match = pattern.match(str(crt_tab_list_arr[i][0]))
        if (match):
            if (crt_tab_list_arr[i][2] == "N"):
                all_str = open_excel(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])
            else:
                all_str = open_excel_with(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])

            des_file = r"C:\Users\Administrator\Desktop\E\%s.hql" % (crt_tab_list_arr[i][1].lower())
            file_write = codecs.open(des_file, 'w', 'utf-8')
            file_write.writelines(all_str)

        else:
            continue
