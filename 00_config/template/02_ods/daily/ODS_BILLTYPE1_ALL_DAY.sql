--目标表：ods.ods_BILLTYPE1
--来源表：src.ods_BILLTYPE1
--作者：
--创建时间：
--更新时间：


drop table if exists ods.src_BILLTYPE1_tmp;
create table ods.src_BILLTYPE1_tmp as
select ID,
src_demo.checkmd5(ID,BILLTYPE,OPMACHINE,OPTIME,OPUSER,CREATEUSER,CREATETIME,ISAFFECT,MEMO) as con_str   ---所有字段
from SRC.SRC_BILLTYPE1
;


--取出新增修改的数据，放到ods.ods_taccstock_tmp2里面;
drop table if exists ods.ods_BILLTYPE1_temp_2;
create table ods.ods_BILLTYPE1_temp_2 as
select t1.ID
from ods.src_BILLTYPE1_tmp T1
left join ods.ods_BILLTYPE1 T2
on t1.con_str = t2.con_str
where t2.con_str is null;


--通过全量ods表和全量src表判断,取出不变和修改的数;
drop table if exists ods.ods_BILLTYPE1_temp_1;
create table ods.ods_BILLTYPE1_temp_1 as
select t1.* 
from ods.ODS_BILLTYPE1 t1
left semi join SRC.SRC_BILLTYPE1  t2
on t1.ID = t2.ID   --主键
;


--取出不变的数据;
drop table if exists ods.ods_BILLTYPE1_temp_3;
create table ods.ods_BILLTYPE1_temp_3 as
select t1.* from ods.ods_BILLTYPE1_temp_1 t1
left join ods.ods_BILLTYPE1_temp_2 t2 
on t1.ID = t2.ID  --主键
where t2.ID is null
;


--插入新增和修改数据;
insert into ods.ods_BILLTYPE1_temp_3
select t2.*,'','2018-02-01' 
from ods.ods_BILLTYPE1_temp_2 t1
join SRC.SRC_BILLTYPE1 t2
on t1.id = t2.id;    --主键
 
drop table ods.ods_BILLTYPE1;
alter table ods.ods_BILLTYPE1_temp_3 rename to ods.ods_BILLTYPE1;

TRUNCATE table ods.ods_BILLTYPE1_temp_1;
TRUNCATE table ods.ods_BILLTYPE1_temp_2;