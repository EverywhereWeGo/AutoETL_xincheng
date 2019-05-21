#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'KD'

import uuid
import xlrd
import codecs
import os
import zipfile
import shutil

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 生成py文件
def record_xml_file(servicetasks, bpmndis, sequenceFlows, dirfile):
    workflow_template = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\05_workflow\xml_workflower")

    sh_cfg = work_book.sheet_by_name("workflow_info")
    process = sh_cfg.cell_value(1, 0)
    name = sh_cfg.cell_value(1, 1)
    startname = sh_cfg.cell_value(1, 2)
    startid = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, str(startname))).replace("-", '')[1:9].upper()

    workflow = workflow_template.replace("{sequenceFlow}", sequenceFlows). \
        replace("{serviceTask}", servicetasks). \
        replace("{bpmndi}", bpmndis). \
        replace("{process}", process). \
        replace("{name}", name). \
        replace("{startid}", startid). \
        replace("{startname}", startname)

    # print workflow

    file_write = codecs.open(dirfile, 'w', 'utf-8')
    file_write.writelines(workflow)
    file_write.close()


def gen_sequenceFlow():
    sequenceFlow_template = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\05_workflow\sequenceFlow")
    sh_cfg = work_book.sheet_by_name("workflow_info")
    nrows_cfg = sh_cfg.nrows

    sequenceFlows = ""
    for i in range(1, nrows_cfg):
        # 判断依赖节点是否为空
        line_name = "线段_" + str(i)
        line_id = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, line_name)).replace("-", '').upper()[1:9]
        sourceRef = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, str(sh_cfg.cell_value(i, 2)))).replace("-", '')[1:9]
        targetRef = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, str(sh_cfg.cell_value(i, 3)))).replace("-", '')[1:9]
        sequenceFlow = sequenceFlow_template.replace("\n", "\n\t\t"). \
            replace("{sourceRef}", sourceRef.upper()). \
            replace("{targetRef}", targetRef.upper()). \
            replace("{id}", line_id). \
            replace("{name}", line_name)

        sequenceFlows = sequenceFlows + sequenceFlow

    print sequenceFlows
    return sequenceFlows


def gen_servicetask_and_bpmndi():
    servicetask_template = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\05_workflow\serviceTask")
    bpmndi_template = read_template_file(
        r"C:\Users\Administrator\Desktop\AutoETL\00_config\template\05_workflow\bpmndi")

    sh_cfg = work_book.sheet_by_name("workflow_list")
    nrows_cfg = sh_cfg.nrows

    servicetasks = ""
    bpmndis = ""
    for i in range(1, nrows_cfg):
        job_name = sh_cfg.cell_value(i, 6).lower()
        job_id = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, str(job_name))).replace("-", '').upper()[1:9]
        job_type = sh_cfg.cell_value(i, 2)
        job_scripttypeid = get_job_scripttypeid(sh_cfg.cell_value(i, 5).upper())
        job_projectid = sh_cfg.cell_value(i, 4)
        job_taskid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(sh_cfg.cell_value(i, 7).lower()))).replace("-", '')
        job_nodeErrorRepeatTimes = str(int(sh_cfg.cell_value(i, 8)))
        job_scriptPara = sh_cfg.cell_value(i, 9)

        servicetask = servicetask_template.replace(",\n", ",").replace("\n", "\n\t\t"). \
            replace("{id}", job_id). \
            replace("{name}", job_name). \
            replace("{type}", job_type). \
            replace("{scriptTypeId}", job_scripttypeid). \
            replace("{projectId}", job_projectid). \
            replace("{taskId}", job_taskid). \
            replace("{nodeErrorRepeatTimes}", job_nodeErrorRepeatTimes). \
            replace("{scriptPara}", job_scriptPara)

        servicetasks = servicetasks + servicetask

        # 生成bpmndi
        x = 200
        y = 200
        x_interval = 80
        y_interval = 80
        bpmndi = bpmndi_template.replace("\n", "\n\t\t\t").replace("{id}", job_id). \
            replace("{x}", str(x + int(i) * x_interval)). \
            replace("{y}", str(y + int(i) * y_interval))
        bpmndis = bpmndis + bpmndi

    # print bpmndis
    print servicetasks
    return (servicetasks, bpmndis)


# 生成zip包
def gen_zip():
    os.remove(r'C:\Users\Administrator\Desktop\workflow.zip')
    newZip = zipfile.ZipFile(r'C:\Users\Administrator\Desktop\workflow.zip', 'a')
    files = get_filelist("C:\Users\Administrator\Desktop\WORKFLOWER")
    for filenames in files:
        shutil.copy(filenames, os.getcwd())

    files = get_filelist(os.getcwd())
    for filenames in files:
        if (filenames.replace("\\", "/") != sys.argv[0]):
            newZip.write(filenames.replace(os.getcwd()+"\\", ""),compress_type=zipfile.ZIP_DEFLATED)
            os.remove(filenames)
    newZip.close()


# 获取指定文件夹下所有脚本名称
def get_filelist(pa):
    Filelist = []
    for home, dirs, files in os.walk(pa):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Filelist


# 读取模板文件
def read_template_file(template_file):
    with open(template_file, 'r') as f:
        template_str = f.read()
    return template_str


# 解析脚本类型
def get_job_scripttypeid(job_scripttype):
    job_scripttypeid = 0
    if (job_scripttype == 'PYTHON'):
        job_scripttypeid = 2
    elif (job_scripttype == 'KHAN'):
        job_scripttypeid = 11
    elif (job_scripttype == 'HIVE'):
        job_scripttypeid = 3
    elif (job_scripttype == 'SHELL'):
        job_scripttypeid = 1
    return str(job_scripttypeid)


if __name__ == '__main__':
    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\AutoETL\00_config\xlsx\workflow.xlsx")
    dir_file = r"C:\Users\Administrator\Desktop\WORKFLOWER\a.xml"

    (st, bi) = gen_servicetask_and_bpmndi()
    sF = gen_sequenceFlow()
    record_xml_file(st, bi, sF, dir_file)
    gen_zip()
