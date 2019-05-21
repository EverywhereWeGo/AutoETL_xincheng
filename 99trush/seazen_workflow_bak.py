#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'KD'

import uuid
import xlrd
import codecs

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 生成线段连接及图表
def gen_line():
    sheet_name_cfg = u"依赖关系设置"
    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name(sheet_name_cfg)
    nrows_cfg = sh_cfg.nrows

    work_flowCode = sh_cfg.cell_value(1, 0)
    work_flowName = sh_cfg.cell_value(1, 1)

    # 初始化数据导入
    sequenceFlow = '''<?xml version='1.0' encoding='UTF-8'?>\n<definitions id="review-definitions" typeLanguage="http://www.w3.org/2001/XMLSchema" expressionLanguage="http://www.w3.org/1999/XPath" targetNamespace="http://activiti.org/bpmn20" xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC" xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:activiti="http://activiti.org/bpmn">\n      <process id="%s" name="%s">\n''' % (
    work_flowCode, work_flowName)
    bpmndi = '''        <bpmndi:BPMNDiagram id="BPMNDiagram_%s">\n          <bpmndi:BPMNPlane id="BPMNPlane_%s" bpmnElement="%s">\n           <bpmndi:BPMNShape id="BPMNShape_Canvas" bpmnElement="BPMNShape_Canvas">
                <omgdc:Bounds width="300" height="300" x="-80" y="-120"/>\n           </bpmndi:BPMNShape>\n''' % (
    work_flowCode, work_flowCode, work_flowCode)

    # 增量数据导入
    # sequenceFlow = '''<definitions id="review-definitions" typeLanguage="http://www.w3.org/2001/XMLSchema" expressionLanguage="http://www.w3.org/1999/XPath" targetNamespace="http://activiti.org/bpmn20" xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC" xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:activiti="http://activiti.org/bpmn">\n
    # <process id="workflow_dataimport_enjoy" name="SRC增量数据导入_昂捷">\n'''
    # bpmndi = '''  <bpmndi:BPMNDiagram id="BPMNDiagram_workflow_dataimport_enjoy">\n
    # <bpmndi:BPMNPlane bpmnElement="workflow_dataimport_enjoy" id="BPMNPlane_workflow_dataimport_enjoy">\n'''

    for i in range(1, nrows_cfg):
        # 判断依赖节点是否为空
        if (sh_cfg.cell_value(i, 3)):
            line_name = "线段_" + str(i)
            # jbpm规则大写字母开头，位数应该也有限制，具体多少不太清楚
            s2 = uuid.uuid3(uuid.NAMESPACE_DNS, sh_cfg.cell_value(i, 2).__str__().lower())
            sourceRef = 'U' + str(s2).replace("-", '').upper()[1:9]
            targetRef = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, sh_cfg.cell_value(i, 3).lower().__str__())).replace(
                "-", '').upper()[1:9]
            line_id = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, line_name)).replace("-", '').upper()[1:9]
            sequenceFlow = sequenceFlow + '             <sequenceFlow sourceRef="' + sourceRef + '" targetRef="' + targetRef + '" id="' + line_id + '" name="' + line_name + '"/>\n'
            # bpmndi = bpmndi + '''      <bpmndi:BPMNEdge id="BPMNEdge_%s" bpmnElement="%s">\n        <omgdi:waypoint x="100" y="100"/>\n        <omgdi:waypoint x="100" y="100"/>\n      </bpmndi:BPMNEdge>\n'''%(line_id,line_id)
    return (sequenceFlow, bpmndi, work_flowCode)


# 生成线段连接及图表
def gen_job():
    sheet_name_cfg = "作业属性设置"
    # 打开导入配置excel，获取详细导入配置
    sh_cfg = work_book.sheet_by_name(sheet_name_cfg)
    nrows_cfg = sh_cfg.nrows
    ncols_cfg = sh_cfg.ncols
    start_job_name = "开始节点"
    start_job_id = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, start_job_name)).replace("-", '').upper()[1:9]
    job_str = '''\n\n           <startEvent id="%s" name="%s"/>\n''' % (start_job_id, start_job_name)
    start_job_name = ""
    bpmndi = '''        <bpmndi:BPMNShape id="BPMNShape_%s" bpmnElement="%s">
                <omgdc:Bounds height="300" width="300" x="200" y="200"/>
         </bpmndi:BPMNShape>\n''' % (start_job_id, start_job_id)
    # 定义x轴，y轴初始化位置
    x = "200"
    y = "200"
    # 定义x轴，y轴的间隔
    x_interval = "80"
    y_interval = "80"
    for i in range(1, nrows_cfg):
        job_scripttypeid = ""
        # 判断作业节点是否为空
        if (sh_cfg.cell_value(i, 5)):
            job_name = sh_cfg.cell_value(i, 6).lower().__str__()
            job_id = 'U' + str(uuid.uuid3(uuid.NAMESPACE_DNS, job_name)).replace("-", '').upper()[1:9]
            job_type = sh_cfg.cell_value(i, 2)
            job_project_name = sh_cfg.cell_value(i, 3)
            job_scripttype = sh_cfg.cell_value(i, 5).upper()
            job_scripttypeid = 0
            print sh_cfg.cell_value(i, 7)
            job_taskid = str(uuid.uuid3(uuid.NAMESPACE_DNS, (sh_cfg.cell_value(i, 7)).lower().__str__())).replace("-",'')

                         # str(uuid.uuid3(uuid.NAMESPACE_DNS, (sh_cfg.cell_value(i, 7)).lower().__str__())).replace("-",'')

            print job_taskid

            if (job_scripttype == 'PYTHON'):
                job_scripttypeid = 2
            elif (job_scripttype == 'KHAN'):
                job_scripttypeid = 11
            elif (job_scripttype == 'HIVE'):
                job_scripttypeid = 3
            elif (job_scripttype == 'SHELL'):
                job_scripttypeid = 1
            job_projectid = sh_cfg.cell_value(i, 4)
            job_nodeErrorRepeatTimes = int(sh_cfg.cell_value(i, 8))
            job_scriptPara = sh_cfg.cell_value(i, 9)
            x_site = int(x) + int(i) * int(x_interval)
            y_site = int(y) + int(i) * int(y_interval)
            job_str = job_str + '''            <serviceTask id="%s" name="%s">
              <extensionElements>
                 <activiti:field name="type">
                   <activiti:expression>%s</activiti:expression>
                 </activiti:field>
                 <activiti:field name="params">
                   <activiti:expression>{"id":"%s","name":"%s","remark":"","scriptTypeId":%s,"projectId":"%s","taskId":"%s","nodeErrorRepeatTimes":"%s","scriptPara":"${%s}","repeatInterval":0,"repeatUnit":"s","scriptParaAc":[],"resultName":"","resultInfo":"","hasSave":true,"validateStr":""}</activiti:expression>
                 </activiti:field>
                 <activiti:field name="remark">
                   <activiti:expression></activiti:expression>
                 </activiti:field>
                 <activiti:field name="message">
                   <activiti:expression></activiti:expression>
                 </activiti:field>
              </extensionElements>
            </serviceTask>\n''' % (
            job_id, job_name, job_type, job_id, job_name, job_scripttypeid, job_projectid, job_taskid,
            job_nodeErrorRepeatTimes, job_scriptPara)
            bpmndi = bpmndi + '''      <bpmndi:BPMNShape id="BPMNShape_%s" bpmnElement="%s">
        <omgdc:Bounds height="30" width="30" x="%s" y="%s"/>
      </bpmndi:BPMNShape>\n''' % (job_id, job_id, x_site, y_site)
    bpmndi = bpmndi + '''    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</definitions>'''
    job_str = job_str + '           </process>\n'
    return (job_str, bpmndi)


# 生成py文件
def record_xml_file(sequence_flow, bpmndi_start, des_file, job_str, bpmndi_end):
    file_write = codecs.open(des_file, 'w', 'utf-8')
    file_write.writelines(sequence_flow)
    file_write.writelines(job_str)
    file_write.writelines(bpmndi_start)
    file_write.writelines(bpmndi_end)
    file_write.close()


if __name__ == '__main__':

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/cms/cms.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/cms/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_customer/xc_customer.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_customer/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_cwy/xc_cwy.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_cwy/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_neighbor/xc_neighbor.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_neighbor/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_order/xc_order.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_order/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_parker/xc_parker.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/工作流/xc_parker/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/src工作流/xc_property/xc_property.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/src工作流/xc_property/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/src工作流/dqmly_dy/dqmly_dy.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/src工作流/dqmly_dy/"


    # ODS
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/cms/cms.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/cms/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/db_temp/db_temp.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/db_temp/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/dqmly_dy/dqmly_dy.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/dqmly_dy/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_customer/xc_customer.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_customer/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_customer/xc_customer.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_customer/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_cwy/xc_cwy.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_cwy/"
    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_neighbor/xc_neighbor.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_neighbor/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_order/xc_order.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_order/"

    # work_book = xlrd.open_workbook(u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_parker/xc_parker.xlsx")
    # dir_file = u"/Users/risheng/bfd/新城/code/数据接入/ods工作流/xc_parker/"

    work_book = xlrd.open_workbook(r"C:\Users\Administrator\Desktop\cms2.xlsx")
    dir_file = r"C:\Users\Administrator\Desktop\asdf"

    # 全部生成
    (sequenceFlow, bpmndi_start, workflow_code) = gen_line()
    des_file = u"%s//%s.xml" % (dir_file, workflow_code)
    (job_str, bpmndi_end) = gen_job()

    record_xml_file(sequenceFlow, bpmndi_start, des_file, job_str, bpmndi_end)
