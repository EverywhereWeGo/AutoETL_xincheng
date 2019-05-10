#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'KD'

import sys
import xlrd
import re
import getpass
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 处理excel，生成建表语句
def open_excel(excel_schema_name, excel_tab_name):
    # excel_schema_name:ODS  excel_tab_name:ODS_TB_CARD_DEF
    sheet_name_tab = excel_schema_name + '_tab_lvl'
    sheet_name_col = excel_schema_name + '_col_lvl'
    # 打开表级excel，获取行值、列值
    sh_tab = work_book.sheet_by_name(sheet_name_tab)
    # 行数35
    nrows_tab = sh_tab.nrows
    # 列数10
    ncols_tab = sh_tab.ncols
    # 打开字段级excel，获取行值、列值
    sh_col = work_book.sheet_by_name(sheet_name_col)
    # 行数906
    nrows_col = sh_col.nrows
    # 列数12
    ncols_col = sh_col.ncols
    insert_str = ''
    # 拼接表级属性
    for i in range(0, nrows_tab):
        if (sh_tab.cell_value(i, 1) == excel_tab_name):
            insert_str = "insert into  " + "ods." + sh_tab.cell_value(i, 1) + "(\n"
            break




    # 拼接表级属性
    # 继续标志，初始为0，如果拼接完SQL后置为1,
    continue_flag = 0
    col_str = ''
    # 字段序号标示
    col_num = 0
    col_str = ""
    dels = ""
    insert_single_str = ""
    select_single_str = ""
    from_str = ""

    # ods第一次全量导入
    # truncate_str = "TRUNCATE TABLE ODS."+excel_tab_name+";\n"
    # ods日常增量进来
    truncate_str = "DELETE FROM ODS." + excel_tab_name + " WHERE ETL_LAD_DTE = '${TX_DATE}';\n"
    for i in range(0, nrows_col):
        if (sh_col.cell_value(i, 2) == excel_tab_name):
            col_num = col_num + 1
            select_single_str = select_single_str + sh_col.cell_value(i, 11) + "\n       ,"
            insert_single_str = insert_single_str + "       " + sh_col.cell_value(i, 6) + ",\n"

            if (col_num == 1):
                # 全量ods
                # from_str = "\nFROM "+sh_col.cell_value(i,9)+"."+sh_col.cell_value(i,10)+" ;\n"
                # 增量ods
                from_str = "\nFROM " + sh_col.cell_value(i, 9) + "." + sh_col.cell_value(i, 10) + ";\n"
                dels = "DELETE FROM ODS." + excel_tab_name + " where " + sh_col.cell_value(i,
                                                                                           11) + " in (select a." + sh_col.cell_value(
                    i, 11) \
                       + " FROM ODS." + excel_tab_name + " a inner join SRC." + sh_col.cell_value(i,
                                                                                                  10) + " b on a." + sh_col.cell_value(
                    i, 11) \
                       + " = b." + sh_col.cell_value(i, 11) + ");\n"
            continue_flag = 1
            continue

        elif ((sh_col.cell_value(i, 1) != excel_tab_name) and (continue_flag == 1)):
            break
        else:
            continue
    select_single_str = "SELECT " + select_single_str
    # 处理掉行字段最后一行的逗号
    select_single_str = select_single_str + "'${TX_DATE}'"
    insert_single_str = insert_single_str + "       ETL_LAD_DTE)\n"
    setdialect_str = "set dialect='default';\n"
    all_str = setdialect_str + truncate_str + dels + insert_str + insert_single_str + select_single_str + from_str
    # print(dels)
    return all_str


# 记录SQL
def record_sql(all_str, file):
    # 指定文件生成路径
    filename = (r"C:\Users\Administrator\Desktop\D\%s.kh") % file.lower()
    file_sql = open(filename, 'w')
    try:
        file_sql.writelines(all_str)
    finally:
        file_sql.close()


# 获取建表sheet页，所需建表的列表
def get_create_tab_list():
    # 打开表级excel，获取行值、列值
    sheet_name_tab = "建表列表"
    sh_crt_tab = work_book.sheet_by_name(sheet_name_tab)
    # 35行
    nrows_crt_tab = sh_crt_tab.nrows
    # 2列
    ncols_crt_tab = sh_crt_tab.ncols
    # 创建二维数组，因第一列不包含，所以长度为列数-1
    create_tab_list = [([0] * ncols_crt_tab) for i in range(nrows_crt_tab - 1)]
    # 从第二列开始遍历，因为第一列为属性注释
    for i in range(1, nrows_crt_tab):
        # 只获取前两列，数据库名和表名
        create_tab_list[i - 1] = [sh_crt_tab.cell_value(i, 0), sh_crt_tab.cell_value(i, 1)]
        # 以下代码为错误测试需要
        # create_tab_list = [sh_crt_tab.cell_value(i,0),sh_crt_tab.cell_value(i,1)]
    return create_tab_list


# 主程序
if __name__ == '__main__':
    excel_name = r"C:\Users\Administrator\Desktop\insert_sel_ods_enjoy.xlsx"
    work_book = xlrd.open_workbook(unicode(excel_name, 'utf-8'))
    # 如果有参数中有需要创建的表名，则创建制定的表名，如果没有创建excel中“建表列表”中的表
    if (len(sys.argv) > 3):
        excel_schema_name = sys.argv[2]
        excel_tab_name = sys.argv[3]
        all_str = open_excel(excel_schema_name, excel_tab_name)
        record_sql(all_str)
    else:
        print("asdf")
        # [['ods', 'ODS_TB_CARD'], ['ods', 'ODS_TB_CARD_DEF']...
        crt_tab_list_arr = get_create_tab_list()
        # 34
        arr_len = len(crt_tab_list_arr)
        for i in range(0, arr_len):
            # 判断当列是否为空，如为空跨过
            pattern = re.compile(r'\w')
            match = pattern.match(str(crt_tab_list_arr[i][0]))
            if (match):
                all_str = open_excel(crt_tab_list_arr[i][0], crt_tab_list_arr[i][1])
                record_sql(all_str, crt_tab_list_arr[i][1])
            else:
                continue
print("All jobs are done")
