#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'KD'

import xlrd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_Group_Value(src_table):
    # 返回四个值，分别是，表名，表有多少列，表序号，表第一个字段开始列
    count = 1
    count_a = 1
    group = {}
    temp = ""
    for i in range(2, work_book_sheet.nrows):
        if (work_book_sheet.cell_value(i, 0)):

            if (work_book_sheet.cell_value(i, 0) == work_book_sheet.cell_value(i - 1, 0)):
                count = count + 1

                temp = (work_book_sheet.cell_value(i, 0) + ',' + str(count) + ',' + str(count_a) + ',' + str(
                    i - count + 1))
            else:

                group.setdefault(work_book_sheet.cell_value(i - 1, 0),
                                 work_book_sheet.cell_value(i - 1, 0) + ',' + str(count) + ',' + str(
                                     count_a) + ',' + str(i - count))
                count_a = count_a + 1
                count = 1

    group.setdefault(temp.split(',')[0], temp)
    return (group[src_table])


def append_primary_key(hql):
    pk = get_Primary_Col_Key(table_name)
    hql.append('ON ')
    for i in range(len(pk)):
        hql.append('t.' + pk[i] + '=t2.' + pk[i])
        if (i + 1 != len(pk)):
            hql.append(' AND ')
    hql.append('\n')


def primary_key_condition(hql, alias, condit):
    pk = get_Primary_Col_Key(table_name)
    for i in range(len(pk)):
        hql.append(alias + pk[i] + condit)
        if (i + 1 != len(pk)):
            hql.append(' and ')


def get_Col_Names(src_table):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    res = []
    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        if (work_book_sheet.cell_value(i, 2).lower() == 'timestamp'):
            res.append('CAST( ' + work_book_sheet.cell_value(i, 1) + ' AS STRING)')
        elif (work_book_sheet.cell_value(i, 2).lower() == 'date'):
            res.append('CAST( ' + work_book_sheet.cell_value(i, 1) + ' AS STRING)')
        elif (work_book_sheet.cell_value(i, 2).lower() == 'int'):
            res.append('CAST( ' + work_book_sheet.cell_value(i, 1) + ' AS int)')
        else:
            res.append(work_book_sheet.cell_value(i, 1))
    return (res)


def get_coalesce_col(src_table):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    res = []
    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        column_name = work_book_sheet.cell_value(i, 1)
        res.append('COALESCE(t.' + column_name + ',t2.' + column_name + ')')
    return (res)


def get_Col_Name(src_table, alias, prefix):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    res = []
    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        column_name = work_book_sheet.cell_value(i, 1)
        res.append(alias + column_name + " AS " + prefix + column_name)
    return (res)


def get_conditions(src_table, alias, prefix, cond, oper):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    res = []
    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        column_name = work_book_sheet.cell_value(i, 1)
        if ('Y' == work_book_sheet.cell_value(i, 3)):
            continue
        if (i == (int(count_end) + int(count_begin) - 1)):
            res.append(alias + column_name + cond + prefix + column_name)
            continue
        res.append(alias + column_name + cond + prefix + column_name + oper)

    return (res)


def get_conditions_castToString(src_table, alias, prefix, cond, oper):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    res = []
    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        column_name = work_book_sheet.cell_value(i, 1)

        if ('Y' == work_book_sheet.cell_value(i, 3)):
            continue
        noteq = '(' + alias + column_name + cond + prefix + column_name + ')'
        leftisnull = '(' + alias + column_name + ' IS NULL AND ' + prefix + column_name + ' IS NOT NULL)'
        rightisnull = '(' + alias + column_name + ' IS NOT NULL AND ' + prefix + column_name + ' IS NULL)'
        if (i == (int(count_end) + int(count_begin) - 1)):
            # res.append(alias + column_name + cond + prefix + column_name)
            res.append('( ' + noteq + ' OR ' + leftisnull + ' OR ' + rightisnull + ' )')
            continue
        res.append('( ' + noteq + ' OR ' + leftisnull + ' OR ' + rightisnull + ' )' + oper)
        # res.append(alias + column_name + cond + prefix + column_name + oper)
    return (res)


def check_Column(src_table, src_col):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]

    for i in range(int(count_begin), int(count_end) + int(count_begin)):
        if (work_book_sheet.cell_value(i, 1) == src_col):
            res = ''
            if (work_book_sheet.cell_value(i, 2).lower() == 'int'):
                res = 0
            elif (work_book_sheet.cell_value(i, 2).lower() == 'varchar'):
                res = '\'\''

            else:
                res = '\'\''

            return (res)


def get_Primary_Col_Key(src_table):
    count_begin = get_Group_Value(src_table).split(',')[3]
    count_end = get_Group_Value(src_table).split(',')[1]
    res = []
    for i in range(int(count_begin), int(count_begin) + int(count_end)):
        if (work_book_sheet.cell_value(i, 3) == 'Y'):  # 判断join不为空

            primary_key = work_book_sheet.cell_value(i, 1)
            res.append(primary_key)
    return (res)


def get_fullDataWithHist(hql, table_name):
    hql.append('hql="\n')
    hql.append('FROM(\n \tselect \n\t\t')
    hql.append('\n\t\t,'.join(get_Col_Name(table_name, 't.', 't_')))
    hql.append('\n\t\t,')
    hql.append('\n\t\t,'.join(get_Col_Name(table_name, 't2.', 't2_')))
    hql.append('\n\t\t,')
    hql.append('\t\tt2.valid_date AS t2_valid_date, \n')
    hql.append('\t\tt2.invalid_date AS t2_invalid_date \n')
    hql.append('\tFROM ' + sys_name + '_src.' + table_name + ' AS t \n')
    hql.append('\tFULL JOIN ( \n')
    hql.append('\t\tSELECT * \n')
    hql.append('\t\tFROM ' + sys_name + '_ods.' + table_name + '\n')
    hql.append("\t\tWHERE data_type='${lat}' AND l_date='${ago_2}'" + '\n')
    hql.append('\t) AS t2 \n')
    print table_name
    pk = get_Primary_Col_Key(table_name)[0]
    # hql.append('\tON t.' + pk + '=t2.' + pk + ' \n')
    # append_primary_key(hql)
    append_primary_key(hql)
    hql.append(') AS t3 \n')

    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(data_type='${del}',l_date='${y_date}') \n")
    hql.append('SELECT \n\t')
    hql.append('\n\t,'.join(get_Col_Name(table_name, 't3.t2_', 't2_')))
    hql.append('\n\t,')
    hql.append('\tt3.t2_valid_date, \n')
    hql.append("\tCAST('${y_date}' AS DATE)\n")
    # hql.append('WHERE\n')
    # hql.append('\tt3.t_' + pk + ' is null \n')
    hql.append('WHERE ')
    primary_key_condition(hql, 't3.t_', ' is null')
    hql.append('\n')

    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(data_type='${ins}',l_date='${y_date}') \n")
    hql.append('SELECT \n\t')
    hql.append('\n\t,'.join(get_Col_Name(table_name, 't3.t_', 't_')))
    hql.append('\n\t,')
    hql.append("\tCAST('${y_date}' AS DATE), \n")
    hql.append("\tCAST('9999-12-31' AS DATE)\n")
    # hql.append('WHERE\n')
    # hql.append('\tt3.t2_' + pk + ' is null \n')
    hql.append('WHERE ')
    primary_key_condition(hql, 't3.t2_', ' is null')
    hql.append('\n')

    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(data_type='${upd}',l_date='${y_date}') \n")
    hql.append('SELECT \n\t')
    hql.append('\n\t,'.join(get_Col_Name(table_name, 't3.t2_', 't2_')))
    hql.append('\n\t,')
    hql.append('\tt3.t2_valid_date, \n')
    hql.append("\tCAST('${y_date}' AS DATE)\n")
    # hql.append('WHERE\n')
    # hql.append('\tt3.t_' + pk + ' is not null and t3.t2_' + pk + ' is not null and ( \n\t')
    hql.append('WHERE ')
    primary_key_condition(hql, 't3.t_', ' is not null')
    hql.append(' AND ')
    primary_key_condition(hql, 't3.t2_', ' is not null')
    hql.append(' AND( \n\t')
    hql.append('\n\t'.join(get_conditions_castToString(table_name, 't3.t_', 't3.t2_', ' != ', ' OR')))
    # hql = hql[:-2]
    hql.append('\n);')
    hql.append('\n"\n')

    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "获取删除、变更或新增数据执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')

    hql.append('\n\n\n')
    # -- 分割线

    hql.append('hql="\n')
    hql.append('WITH ${upd} AS ( \n')
    hql.append('\tSELECT\n')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append('\n\t\t,')
    hql.append("\t\tCAST('${y_date}' as DATE),\n")
    hql.append("\t\tCAST('9999-12-31' as DATE)\n")
    hql.append("\tFROM " + sys_name + '_src.' + table_name + '\n')
    hql.append('\t WHERE ' + pk + ' IN ( \n')
    hql.append('\t\tSELECT\n')
    hql.append('\t\t\tt1.' + pk + ' as u' + pk + '\n')
    hql.append('\t\tFROM ' + sys_name + '_ods.' + table_name + ' as t1 \n')
    hql.append("\t\tWHERE t1.data_type='${upd}' AND t1.l_date='${y_date}' \n")
    hql.append('\t)\n')
    hql.append('),\n')

    hql.append('${lat}WithOutUpd AS ( \n')
    hql.append('\tSELECT\n')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append('\n\t\t,')
    hql.append("\t\tvalid_date,\n")
    hql.append("\t\tinvalid_date\n")
    hql.append("\tFROM " + sys_name + '_ods.' + table_name + '\n')
    hql.append("\t WHERE data_type='${lat}' AND l_date='${ago_2}' AND " + pk + ' NOT IN ( \n')
    hql.append('\t\tSELECT\n')
    hql.append('\t\t\tt2.' + pk + ' as o' + pk + '\n')
    hql.append('\t\tFROM ' + sys_name + '_ods.' + table_name + ' as t2 \n')
    hql.append("\t\twhere (t2.data_type='${upd}' or t2.data_type='${del}') and t2.l_date='${y_date}' \n")
    hql.append('\t)\n')
    hql.append('),\n')

    hql.append('${ins} AS ( \n')
    hql.append('\tSELECT\n')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append('\n\t\t,')
    hql.append("\t\tvalid_date,\n")
    hql.append("\t\tinvalid_date\n")
    hql.append("\tFROM " + sys_name + '_ods.' + table_name + '\n')
    hql.append("\twhere data_type='${ins}' and l_date='${y_date}'\n)\n")

    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(data_type='${lat}',l_date='${y_date}') \n")
    hql.append('SELECT * FROM ${upd} \n')
    hql.append('UNION ALL \n')
    hql.append('SELECT * FROM ${lat}WithOutUpd \n')
    hql.append('UNION ALL \n')
    hql.append('SELECT * FROM ${ins} \n')
    hql.append(';\n')

    hql.append('"\n')
    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "数据整合HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')

    hql.append('hql="\n')
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${del}',l_date<='${clean_del_parti}');\n")
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${upd}',l_date<='${clean_upd_parti}');\n")
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${ins}',l_date<='${clean_ins_parti}');\n")
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${lat}',l_date<='${clean_lat_parti}');\n")
    hql.append('"\n')
    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "数据整合HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')


def get_fullDataWithOutHist(hql, table_name):
    hql.append('hql="\n')
    hql.append('INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + '\n')
    hql.append('SELECT\n\t')
    hql.append('\n\t,'.join(get_Col_Names(table_name)))
    hql.append('\n')
    hql.append('FROM ' + sys_name + '_src.' + table_name + '\n')
    hql.append(';\n"\n')

    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')


def get_increDataWithOutHist(hql, table_name):
    hql.append('hql="\n')
    hql.append('INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(l_date='${y_date}')" + '\n')
    hql.append('SELECT \n\t')
    hql.append('\n\t,'.join(get_coalesce_col(table_name)))
    hql.append('\nFROM ' + sys_name + '_src.' + table_name + ' AS t \n')
    hql.append('FULL JOIN ( \n')
    hql.append('\tSELECT\n\t\t')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append('\n\tFROM ' + sys_name + '_ods.' + table_name + '\n')
    hql.append("\tWHERE l_date='${ago_2}' \n")
    hql.append(') as t2 \n')
    append_primary_key(hql)

    hql.append(';\n"\n')

    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')


def get_increDataWithHist(hql, table_name):
    hql.append('hql="\n')
    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION(data_type='${chg}',l_date='${y_date}') \n")
    hql.append('SELECT \n\t')
    hql.append('\n\t,'.join(get_Col_Names(table_name)))
    hql.append(',\n\tvalid_date,')
    hql.append("\n\tCAST('${y_date}' as DATE)")
    hql.append('\nFROM ' + sys_name + '_ods.' + table_name + '\n')
    pk = get_Primary_Col_Key(table_name)[0]
    hql.append("WHERE data_type='${lat}' and l_date='${ago_2}' and " + pk + ' in ( \n')
    hql.append('\tSELECT\n')
    hql.append('\t\tt.' + pk + ' as uid \n')
    hql.append('\tFROM ' + sys_name + '_src.' + table_name + ' as t\n')
    hql.append(')\n')
    hql.append(';\n"\n')

    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "获取更新数据失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')

    hql.append('\n\n\n')

    hql.append('hql="\n')
    hql.append('WITH ${lat}WithOutUpd AS( \n')
    hql.append('\tSELECT\n\t\t')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append(',\n\t\tvalid_date,')
    hql.append('\n\t\tinvalid_date\n')
    hql.append('\tFROM ' + sys_name + '_ods.' + table_name)
    hql.append("\n\t WHERE data_type='${lat}' AND l_date='${ago_2}' and " + pk + ' not in (\n')
    hql.append('\t\tSELECT\n')
    hql.append('\t\t\tt.' + pk + ' as uid \n')
    hql.append('\t\tFROM ' + sys_name + '_src.' + table_name + ' as t \n')
    hql.append('\t)\n')
    hql.append('),\n')
    hql.append('increData as ( \n')
    hql.append('\tSELECT\n\t\t')
    hql.append('\n\t\t,'.join(get_Col_Names(table_name)))
    hql.append(",\n\t\tCAST('${y_date}' as DATE),")
    hql.append("\n\t\tCAST('9999-12-31' as DATE)\n")
    hql.append('\tFROM ' + sys_name + '_src.' + table_name)
    hql.append('\n)\n')
    hql.append(
        'INSERT OVERWRITE TABLE ' + sys_name + '_ods.' + table_name + " PARTITION (data_type='${lat}',l_date='${y_date}')\n")
    hql.append('SELECT * FROM ${lat}WithOutUpd \n')
    hql.append('UNION ALL \n')
    hql.append('SELECT * FROM increData \n')
    hql.append(';\n"\n')

    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "数据整合HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')

    hql.append('hql="\n')
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${chg}',l_date<='${clean_ins_parti}');\n")
    hql.append(
        'ALTER TABLE ' + sys_name + '_ods.' + table_name + " DROP IF EXISTS PARTITION(data_type='${lat}',l_date<='${clean_lat_parti}');\n")
    hql.append('"\n')
    hql.append('echo "${hql}"\n')
    hql.append('hive -e "${hql}"\n')
    hql.append('if [ $? != 0 ]\n')
    hql.append('then\n')
    hql.append('\techo "数据整合HQL执行失败！"\n')
    hql.append('\texit 1\n')
    hql.append('fi\n')


if __name__ == '__main__':
    sys_name = 'oa'
    path = unicode(r"C:\Users\Administrator\Desktop\上海新城项目\工作流脚本批量导入_同策\insert\ODS日常全量\tospur_oa.xlsx", 'utf-8')
    model_path = "C:\Users\Administrator\Desktop\D\\"

    work_book_sheet = xlrd.open_workbook(path).sheet_by_name('对应关系表')
    model_name = xlrd.open_workbook(path).sheet_by_name('目录')

    for i in range(1, model_name.nrows):
        if (model_name.cell_value(i, 1) == 1):
            print(model_name.cell_value(i,1))
            sh = []
            hql = []
            etl_name = ""
            table_name = ""
            etl_name = model_path + 'ods_' + model_name.cell_value(i, 0) + '.sh'
            print etl_name
            table_name = model_name.cell_value(i, 0)
            print table_name
            ods_model = model_name.cell_value(i, 2)

            if (ods_model == 1):
                # 每日全量接入，保存历史数据
                get_fullDataWithHist(hql, table_name)
            elif (ods_model == 2):
                # 每日全量接入，不保存历史数据
                get_fullDataWithOutHist(hql, table_name)
            elif (ods_model == 3):
                # 每日增量接入，保存历史数据
                get_increDataWithHist(hql, table_name)
            elif (ods_model == 4):
                # 每日增量接入，不保存历史数据
                get_increDataWithOutHist(hql, table_name)
            else:
                print 'ERROR:请检查ods类型'
                exit(1)

            print(table_name + ' run ok!\n')

            sh.append('#!/bin/bash\n')
            sh.append('source ./get_date.sh\n')
            sh.append('source ./config.sh\n')
            # 生成脚本
            output = open(etl_name, 'w')
            for s in (sh):
                output.write(s)

            for aa in (hql):
                print(aa)
                output.write(aa)
            output.close()
