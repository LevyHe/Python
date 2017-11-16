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
import re,time,threading
import MySQLdb
import datetime
import sys
from thread_test import get_flight_state as get_flight_state
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
def refresh_flights_list():
  try:
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return
    sql = '''delete from flights_list_run;
    insert into flights_list_run(`flight_no`,`flt_type`,`pd_time`,`pa_time`,`aa_time`,`ad_time`,`w_state`,`l_state`,`type`,`desc_state`,`update_time`)
    select *,now() from flights_list;'''
    cur = vdgs_test.cursor()
    cur.execute(sql)
    cur.close()
    vdgs_test.close()
  except Exception as e:
    print('Unable connect to remounte server:', e)  
    return     

def get_image_form_socket():
  server_addr=('192.168.1.96',5012)
  try:
    import socket
    from select import select  
    clent_fd = socket.create_connection(server_addr,timeout=4)
    if clent_fd is None:
      return None
    slen=clent_fd.sendall("vdgs:image")
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
    if data:
      return data[1],data[2]
    else :
      return None,None
  except Exception as e:
    print('Unable  connetct to  58.211.162.30 :', e)    
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
    print('Unable  connetct to  58.211.162.30 :', e)  

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
    global flight_list
    if flight=='' or flight is None:
      return
    flight=str(flight)
    if flight in flight_list.keys():    
      flight_list[flight].update(kwargs)
    vdgs_test=vdgs_upload_connnection()
    if vdgs_test is None:
      return
    set_value=','.join([str(k)+"='"+str(v)+"'" for k,v in kwargs.items()])
    cur = vdgs_test.cursor()
    sql = str("update flights_list_run set %s ,update_time=now() where flight_no='%s';"%(set_value,flight))
    #print sql
    cur.execute(sql)
    cur.close()
    vdgs_test.close()
  except Exception as e:
    print('Unable connect to remounte server:', e)  
       
flight_list={} 
def main():
  global flight_list
  always_run=True
  isnewdayrun=True
  days_changed=False
  last_lead_state=0  #0空闲，1等待，
  
  while always_run:
    try:
      time_now=time.strftime("%H:%M", time.localtime())
      if time_differ(time_now,'05:00')>0 and time_differ(time_now,'05:05')<0:
        days_changed=True
      if days_changed and time_differ(time_now,'05:12')>0:
        days_changed=False
        isnewdayrun=True      
      if isnewdayrun or flight_list is None:
        isnewdayrun=False
        refresh_flights_list()
        flight_list=get_flishts_list()
   
      flight,isleadcmd,leadstate=get_work_state()
      #jpg=get_image_form_socket()
      #if jpg and leadstate is not None:
      #  update_vdgs_state(lead_state=leadstate,image=jpg)
      
      if leadstate is not None and leadstate!=last_lead_state:
        if leadstate in [1,2,3,4] and last_lead_state ==0:
          update_flights_state(flight,l_state=1)
        elif leadstate==5:
          update_flights_state(flight,l_state=2,aa_time=time_now,desc_state="引导完成")
        elif leadstate==0:
          upload_lead_history()
          for k,v in flight_list.items():
            if v['l_state']==2:
              update_flights_state(k,l_state=3,ad_time=time_now,desc_state="飞机离岗")
              break
        last_lead_state=leadstate
      if isleadcmd is not None and not isleadcmd and flight_list:
        date_today=time.strftime("%Y%m%d", time.localtime())
        for i, flt in flight_list.items():      
          url='http://flights.ctrip.com/actualtime/fno--'+flt['flight_no']+'-'+date_today+'.html'
          pl_time=flt['pd_time']
          # pa_time=flt['parrival']
          time_now=time.strftime("%H:%M", time.localtime())
          if int(flt['l_state']) in [0,1]:
            if time_differ(time_now,pl_time)>30:
              state,atime=get_flight_state(url,int(flt['type']))
              #print(time_now,flt['flight_no'],flt['flt_type'],atime,state)           
              if state==1 and atime and time_differ(atime,time_now)<15:              
                set_lead_cmd(flt['flight_no'],flt['flt_type'])
                update_flights_state(flt['flight_no'],l_state=1,w_state=state,desc_state="等待接机")
              elif state==2:
                update_flights_state(flt['flight_no'],l_state=4,w_state=state,desc_state="已经到达")
              elif state==3:
                update_flights_state(flt['flight_no'],w_state=state,desc_state="飞机延误")
              elif state==4:
                update_flights_state(flt['flight_no'],l_state=4,w_state=state,desc_state="航班取消")
              elif state ==1:
                update_flights_state(flt['flight_no'],w_state=state,desc_state="已经起飞")            
              time.sleep(15)
        time.sleep(30)
      else:
        time.sleep(10)
    except Exception as e:
      print('main process has error:', e)    
def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()
    
if __name__=='__main__':
  th1=threading.Thread(target=update_vdgs_thread)
  th1.setDaemon(True)
  th1.start()
  main()
  
  if not 0:
    print 1111
  else :
    print 1000
  
  
  
  
  
  
  
  
  
  
  
  
  
