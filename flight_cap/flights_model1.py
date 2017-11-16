#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:37:38 2017

@author: levy
"""

''' state 0 计划
          1  起飞
          2   到达
          3   延误'''
import re,time,threading,signal
import MySQLdb
import datetime
import sys
from thread_web import get_flight_state as get_flight_state
#class flights(object):
#  def __init__(self):
#    pass
#  

def vdgs_local_connection():
  try:
    conn= MySQLdb.connect(
            host='192.168.1.96',
            port = 3306,
            user='vdgs',
            passwd='vdgs20161121',
            db ='VDGS',
            connect_timeout=20,
            autocommit=True
            )
    return conn
  except Exception as e:
    print ("can not connect to 192.168.1.96 ",e)
    return None

def vdgs_upload_connnection():
  try:
    vdgs_test=MySQLdb.connect(
            host='58.211.162.30',
            port = 3306,
            user='vdgs',
            passwd='vdgs_20171121',
            db ='vdgs_test',
            charset="utf8",
            connect_timeout=20,
            autocommit=True
            )
    return vdgs_test
  except Exception as e:
    print ("can not connect to 58.211.162.30 ",e)
    return None

def vdgs_excute_none(sql):
  try:
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return 
    cur=vdgs_test.cursor()
    cur.execute(sql)
    cur.close()
    vdgs_test.close()
  except Exception as e:
    print('vdgs_excute_none error:', e)    
    return None,None
  
  
def refresh_flights_list_weh1():
  global flights_list_weh
  try:
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return False
    sql=''' insert into flights_list_weh1_history(`flight_no`,`flt_type`,`berth_no`,`f_from`,`f_to`,`pf_time`,`pa_time`,`ef_time`,`ea_time`,
    `af_time`,`aa_time`,`in_time`,`out_time`,`w_state`,`l_state`,`type`,`desc_state`,`f_date`,`id`)
    select *,now(),0 from flights_list_weh2;
	delete from flights_list_weh2;'''
    cur = vdgs_test.cursor()
    cur.execute(sql)
    cur.close()
    vdgs_test.close()
    flights_list_weh={}
    return True
  except Exception as e:
    print('refresh_flights_list_weh1 error:', e)  
    return False

def get_image_form_socket():
  server_addr=('192.168.1.96',5012)
  try:
    import socket
    from select import select  
    clent_fd = socket.create_connection(server_addr,timeout=4)
    if clent_fd is None:
      return None
    clent_fd.sendall("vdgs:image")
    header=clent_fd.recv(16)
    if header:
      reg=re.findall(r"\d+",header) 
      image_size=int(reg[0])
      recv_size=0
      image_buf=b""
      input_list = [clent_fd]     
      while recv_size<image_size:
        iobj,_,_=select(input_list,[],[],1)
        if iobj is None:
          break
        image_data=clent_fd.recv(1024)
        recv_size+=len(image_data)
        image_buf+=image_data
      clent_fd.close()
      if recv_size<image_size:
        return None
      else :
        return image_buf
    else:
      return None
  except Exception as e:
    print('Unable  get image :', e)  
    return None
  
def get_flishts_list():
  try:
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return None   
    cur=vdgs_test.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("select * from flights_list_run;")
    data=cur.fetchall()
    cur.close
    vdgs_test.close()
    return dict([(str(x['flight_no']),x) for x in data])
  except Exception as e:
    print('Unable connect to remounte server:', e)  
    return None
def upload_lead_history():
  try:
    conn=vdgs_local_connection()
    if conn is None:
      return
    cur_l=conn.cursor()
    cur_l.execute("SELECT * FROM VDGS.HY_VDGS_LeadHistory order by ID desc limit 1;")
    data=cur_l.fetchone()
    cur_l.close()  
    conn.close()
    data = ','.join([str("'"+str(x)+"'") for x in data[1:]])
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return
    cur_r=vdgs_test.cursor()
    cur_r.execute("insert into flights_history values (0,"+ data+");")
    cur_r.close()
    vdgs_test.close()
  except Exception as e:
    print('Unable connect to remounte server:', e)  
    return 

def set_lead_cmd(flight,flt_type):
  try:
    conn=vdgs_local_connection()
    if conn is None:
      return
    cur = conn.cursor()
    cur.execute("INSERT INTO `VDGS`.`HY_VDGS_LeadCmd` VALUES(0,'VD0009','','%s','%s',0,0,0,0,2,now());"%(flight,flt_type))
    cur.close()
  except Exception as e:
    print('Unable connect to local server:', e)  
def get_work_state():
  try:  
    conn=vdgs_local_connection()
    if conn is None:
      return None,None,None
    cur = conn.cursor()
    cur.execute("select * from HY_VDGS_LeadState;")
    data=cur.fetchone()
    cur.close()
    return data[4],ord(data[11]),data[15]
  except Exception as e:
    print('Unable connect to local server:', e)  
    return None,None,None
berth_state=0 #0空闲，1占用

def time_differ(time1,time2):
  try:
    time1=datetime.datetime.strptime(time1,"%H:%M")
    time2=datetime.datetime.strptime(time2,"%H:%M")
    dif_time=time1-time2
    return dif_time.total_seconds()/60
  except Exception as e:
    print(' time_differ:', e)  
    return None
def vdgs_get_lead_cmd():
  try:
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return None,None
    cur=vdgs_test.cursor()
    cur.execute("select * from flights_lead_cmd limit 1;")
    data=cur.fetchone()
    cur.execute("delete from flights_lead_cmd where id is not null; ")
    cur.close()
    vdgs_test.close()
    if data:
      return data[1],data[2]
    else :
      return None,None
  except Exception as e:
    print('vdgs_get_lead_cmd error :', e)    
    return None,None
def update_vdgs_state(**kwargs):
  try:
    keys =','.join([str(k)+"=%s" for k in kwargs.keys()])
    args=tuple(kwargs.values())
    if not keys:
      return
    vdgs_test=vdgs_upload_connnection()
    cur=vdgs_test.cursor()
    sql = "update vdgs_states_value set "+keys+",run_count=run_count+1,update_time=now() where id = 1 ;"
    print sql
    cur.execute(sql,args)
    cur.close() 
    vdgs_test.close()
  except Exception as e:
    print('update_vdgs_state error :', e)  

def update_vdgs_thread():
  while True:
    try:
      flight,isleadcmd,leadstate=get_work_state()
      if not isleadcmd:
        flt_no,flt_type= vdgs_get_lead_cmd()
        if flt_type:
          set_lead_cmd(flt_no,flt_type)
      jpg=get_image_form_socket()
      
      if jpg and leadstate is not None:
        print(len(jpg),leadstate)
        update_vdgs_state(lead_state=leadstate,image=jpg)
      elif  leadstate is not None:
        update_vdgs_state(lead_state=leadstate)       
      time.sleep(20)
    except Exception as e:
      print ("update_vdgs_thread error ",e)
  
  
           
def update_flights_state(flight,**kwargs):
  try:
    global flights_list_weh
    if flight=='' or flight is None:
      return
    flight=str(flight)
    if flight in flights_list_weh.keys():    
      flights_list_weh[flight].update(kwargs)
    set_value=','.join([str(k)+"='"+str(v)+"'" for k,v in kwargs.items()])
    sql = str("update flights_list_weh2 set %s where flight_no='%s';"%(set_value,flight))
    return sql
  except Exception as e:
    print('update_flights_state error:', e)
    return ''
       
flight_actype=None
flights_list_weh={}
last_lead_state=0

def flights_flt_type(flights):
  try:
    global flight_actype
    if flight_actype is None:
      flight_actype={}
      with open('aa1.csv','rb') as f:
        for line in f.readlines():
          flight_actype[line.split(',')[0]]=line.split(',')[1].strip()  
    if (flights in flight_actype.keys()):
      return flight_actype[flights]
    else:
      return 'B737S'
  except  Exception as e:
    print ("try_str_time error ",e)
    return 'B737S'
def try_str_time(val):
  try:
    if val and val.strip():
      time.strptime(str(val), "%H:%M")
      return str(val)
    else:
      return ''
  except  Exception as e:
    print ("flights_flt_type error ",e)
    return ''
def try_string(val):
  try:
    return str(val)
  except  Exception as e:
    print ("try_string error ",e)
    return ''
def unicode_stae(val):
  state=None
  try:
    if  u'起飞' == unicode(val):
      state=1
    elif  u'到达' == unicode(val): 
      state=2
    elif  u'延误' == unicode(val): 
      state=3
    elif u'取消' == unicode(val):  
      state=4  
    else:
      state=0
    return state
  except  Exception as e:
    print ("unicode_stae error ",e)
    return None  
def flights_process():
  global last_lead_state
  try:
    fls=get_flight_state()  
    sql_build=''
    if fls is not None:
      for fl in fls.values():
        fdt={}
        fdt['flight_no']=fl[0].encode("utf-8")  
        fdt['flt_type']=flights_flt_type(try_string(fl[0]))
        fdt['berth_no']=fl[3].encode("utf-8")  
        fdt['f_from']=fl[1].encode("utf-8")
        fdt['f_to']=fl[2].encode("utf-8")
        fdt['pf_time']=try_str_time(fl[4])
        fdt['pa_time']=try_str_time(fl[5])
        fdt['ef_time']=try_str_time(fl[6])
        fdt['ea_time']=try_str_time(fl[7])
        fdt['af_time']=try_str_time(fl[8])
        fdt['aa_time']=try_str_time(fl[9])   
        fdt['w_state']=unicode_stae(fl[10])
        fdt['type']=1
        if (try_string(fl[0])  not in flights_list_weh.keys()):
          fdt['in_time']=''
          fdt['out_time']=''           
          fdt['l_state']=0     
          fdt['desc_state']='未执行' 
          flights_list_weh[try_string(fl[0])]=fdt
          s_key= ','.join([try_string("`"+try_string(x)+"`") for x in fdt.keys()])
          s_val = ','.join([try_string("'"+try_string(x)+"'") for x in fdt.values()])
          s="replace into flights_list_weh2 (%s) values(%s);"%(s_key,s_val)
          sql_build=sql_build+s
        else:
          fdt1=flights_list_weh[try_string(fl[0])]
          fdt['in_time']=fdt1['in_time']
          fdt['out_time']=fdt1['out_time']          
          fdt['l_state']=fdt1['l_state']
          fdt['desc_state']=fdt1['desc_state']   
          if cmp(fdt,fdt1)==0:
            continue
          if fdt['l_state']==0:
            if fdt['w_state']==1:
              fdt['desc_state']='已经起飞'
            elif fdt['w_state']==2:
              fdt['desc_state']='已经到达'
            elif fdt['w_state']==3:
              fdt['desc_state']='飞机延误'
            elif fdt['w_state']==4:
              fdt['desc_state']='航班取消'
              fdt['l_state']=4
          flights_list_weh[try_string(fl[0])]=fdt
          ss=','.join([try_string(k)+"='"+try_string(v)+"'" for k, v in fdt.items()])
          s="update flights_list_weh2 set %s where flight_no='%s';"%(ss,fdt['flight_no'])
          sql_build=sql_build+s    
    flight,isleadcmd,leadstate=get_work_state()
    if leadstate is not None and leadstate!=last_lead_state:
      if leadstate in [1,2,3,4] and last_lead_state ==0:
        sql_build+=update_flights_state(flight,l_state=1)
      elif leadstate==5:
        time_now=time.strftime("%H:%M", time.localtime())
        sql_build+=update_flights_state(flight,l_state=2,in_time=time_now,desc_state="引导完成")
      elif leadstate==0:
        upload_lead_history()
        for k,v in flights_list_weh.items():
          if v['l_state']==2:
            time_now=time.strftime("%H:%M", time.localtime())
            sql_build+=update_flights_state(k,l_state=3,out_time=time_now,desc_state="飞机离岗")
            break
      last_lead_state=leadstate    
    
    if isleadcmd==0 and flights_list_weh:
      for key,val in  flights_list_weh.items():
        if val['l_state'] not in [0,1]:
          continue
        time_now=time.strftime("%H:%M", time.localtime())
        if val['w_state']==1 and val['ea_time'] and time_differ(val['ea_time'],time_now)<15:
          set_lead_cmd(val['flight_no'],val['flt_type'])
          sql_build+=update_flights_state(key,l_state=1,desc_state="等待接机")
          break
        elif val['w_state']==2 and val['aa_time'] and time_differ(time_now,val['aa_time'])<10:
          set_lead_cmd(key,val['flt_type'])
          sql_build+=update_flights_state(key,l_state=1,desc_state="等待接机")
          break
        elif val['w_state']==2:
          sql_build+=update_flights_state(key,l_state=4,desc_state="已经到达")
    if sql_build:
      vdgs_excute_none(sql_build)
    print (flights_list_weh.keys(),time.strftime("%H:%M:%S", time.localtime()))
  except Exception as e:
    print('flights_process error:', e) 


def main():
  always_run=True
  isnewdayrun=True
  days_changed=False
  
  while always_run:
    try:
      time_now=time.strftime("%H:%M", time.localtime())
      if time_differ(time_now,'05:00')>0 and time_differ(time_now,'05:05')<0:
        days_changed=True
      if days_changed and time_differ(time_now,'05:12')>0:
        days_changed=False
        isnewdayrun=True      
      if isnewdayrun :        
        if refresh_flights_list_weh1():
          print ("refresh_flights_list_weh1...")
          isnewdayrun=False
   
      flights_process()
      time.sleep(30)
    except Exception as e:
      print('main process has error:', e)    
def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()
    
if __name__=='__main__':
  signal.signal(signal.SIGINT, quit)
  signal.signal(signal.SIGTERM, quit)
  th1=threading.Thread(target=update_vdgs_thread)
  th1.setDaemon(True)
  th1.start()
  main()

  
  
  
  
  
  
  
  
  
  
  
  
  
