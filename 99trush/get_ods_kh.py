#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'KD'

import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_Group_Value(src_table):
#返回四个值，分别是，表名，表有多少列，表序号，表第一个字段开始列             
    count=1
    count_a=1
    group={}
    temp=""
    for i in range(2,work_book_sheet.nrows):   
        if(work_book_sheet.cell_value(i,0)):
                         
            if (work_book_sheet.cell_value(i,0)==work_book_sheet.cell_value(i-1,0)):
                count=count+1
              
                temp=(work_book_sheet.cell_value(i,0)+','+str(count)+','+str(count_a)+','+str(i-count+1))
            else:
                
                group.setdefault(work_book_sheet.cell_value(i-1,0),work_book_sheet.cell_value(i-1,0)+','+str(count)+','+str(count_a)+','+str(i-count))
                count_a=count_a+1
                count=1
    
    group.setdefault(temp.split(',')[0],temp)      
    return (group[src_table])
    
def get_Col_Name(src_table):
    
    count_begin=get_Group_Value(src_table).split(',')[3]
    count_end=get_Group_Value(src_table).split(',')[1]
    
    res=[]
    for i in range(int(count_begin),int(count_end)+int(count_begin)):       
        
        res.append(work_book_sheet.cell_value(i,1))
    return (res)
    

def check_Column(src_table,src_col):
    
    count_begin=get_Group_Value(src_table).split(',')[3]
    count_end=get_Group_Value(src_table).split(',')[1]
    
    
    for i in range(int(count_begin),int(count_end)+int(count_begin)):       
        if (work_book_sheet.cell_value(i,1)==src_col):
            res=''
            if (work_book_sheet.cell_value(i,2).lower()=='int'):
                res=0
            elif(work_book_sheet.cell_value(i,2).lower()=='varchar'):
                res='\'\''
                
            else:
                res='\'\''
           
            return (res)
    
        
def get_Primary_Col_Key(src_table):
    count_begin=get_Group_Value(src_table).split(',')[3]
    count_end=get_Group_Value(src_table).split(',')[1]
    res=[]
    for i in range(int(count_begin),int(count_begin)+int(count_end)):       
        if (work_book_sheet.cell_value(i,3)=='Y'):    #判断join不为空
                 
            primary_key=work_book_sheet.cell_value(i,1)
            res.append(primary_key)           
    return(res)
   

    
if __name__ == '__main__':
    path=unicode(r"C:\Users\Administrator\Desktop\ODS日常全量_XCS_补充.xlsx", 'utf-8')
    #脚本生成目录
    model_path=unicode(r"C:\Users\Administrator\Desktop\ods_test\\", 'utf-8')
    work_book_sheet=xlrd.open_workbook(path).sheet_by_name('对应关系表')  
    model_name=xlrd.open_workbook(path).sheet_by_name('目录')  

    for i in range(1,model_name.nrows):

        if (model_name.cell_value(i,1)==1):
           # print(model_name.cell_value(i,1))
            kh=[]
            etl_name=""
            table_name=""
            etl_name=model_path+'ODS_'+model_name.cell_value(i,0)+'_ALL_DAY.kh'
            table_name = model_name.cell_value(i,0)
           
            kh.append('set dialect=\'default\';\n')
            kh.append('--取出新增修改的数据，放到ods.ods_taccstock_tmp2里面;\n')
            kh.append('drop table if exists ods.' + table_name + '_temp_2;' + '\n')
            kh.append('create table ods.'+table_name+'_temp_2 as '+'\n')
            kh.append('select\n')
            temp_kh=[]
            for a in (get_Col_Name(table_name)):
                
                temp_kh.append('coalesce(t1.'+a+','+str(check_Column(table_name,a))+')')                
            kh.append('\n,'.join(temp_kh))
            kh.append('\n')
            kh.append('from src.src_'+table_name+' T1\n')
            kh.append('left join ods.ods_'+table_name+' T2\n')
            kh.append('on 1=1\n')
            temp_kh=[]
            for b in (get_Col_Name(table_name)):
                kh.append('and coalesce(t1.'+b+','+str(check_Column(table_name,b))+')=coalesce(t2.'+b+','+str(check_Column(table_name,b))+')\n')
            kh.append('where t2.'+b+' is null;\n')
            kh.append('\n'*3)
            kh.append('--通过全量ods表和全量src表判断,取出不变和修改的数;\n')
            kh.append('drop table if exists ods.' + table_name + '_temp_1;' + '\n')
            kh.append('create table ods.ods_'+table_name+'_temp_1 as\n')
            kh.append('select * from ods.ODS_'+table_name+' t1\n')
            kh.append(' where exists (select 1 from src.SRC_'+table_name+'  t2\n')
            kh.append('where 1=1\n')
            
            for c in (get_Primary_Col_Key(table_name)):
                kh.append('and coalesce(t1.'+c+','+str(check_Column(table_name,c))+')=coalesce(t2.'+c+','+str(check_Column(table_name,c))+')\n')
            kh.append(');\n')
            kh.append('drop table ods.ods_' + table_name + ';\n');
            kh.append('alter table ods.ods_' + table_name + '_temp_1 rename to ods_' + table_name + ';\n')

            kh.append('\n'*3)
            kh.append('--取出不变的数据;\n')
            kh.append('drop table if exists ods.' + table_name + '_temp_3;' + '\n')
            kh.append('create table ods.ods_'+table_name+'_temp_3 as\n')
            kh.append('select * from ods.ods_'+table_name+' t1\n')
            kh.append('where not exists (select 1 from ods.ods_'+table_name+'_temp_2 t2 \n')
            kh.append('where 1=1 \n')
            for d in (get_Primary_Col_Key(table_name)):
                kh.append('and coalesce(t1.'+d+','+str(check_Column(table_name,d))+')=coalesce(t2.'+d+','+str(check_Column(table_name,d))+')\n')
            kh.append(');\n')

            kh.append('drop table ods.ods_'+table_name+';\n');
            kh.append('alter table ods.ods_'+table_name+'_temp_3 rename to ods_'+table_name+';\n')
            kh.append('\n'*3)
            kh.append('--插入新增和修改数据;\n')
            kh.append('insert into ods.ods_'+table_name+'\n')
            kh.append('select * from ods.ods_'+table_name+'_temp_2;\n')
            kh.append('\n'*2)
            kh.append('TRUNCATE table ods.ods_'+table_name+'_temp_2;\n')


            print(table_name+' run ok!\n')
            #生成脚本            
            output = open(etl_name, 'w')
            for aa in (kh):
                #print(aa,end="")
                output.write(aa)
            output.close()

    
