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
from six.moves import cPickle as pickle
import re,time,csv
from selenium import webdriver
import MySQLdb
import datetime



def vdgs_local_connection():
  conn= MySQLdb.connect(
          host='192.168.1.96',
          port = 3306,
          user='vdgs',
          passwd='vdgs20161121',
          db ='VDGS',
          connect_timeout=2,
          autocommit=True
          )
  return conn
def vdgs_upload_connnection():
  vdgs_test=MySQLdb.connect(
          host='58.211.162.30',
          port = 3306,
          user='vdgs',
          passwd='vdgs_20171121',
          db ='vdgs_test',
          charset="utf8",
          connect_timeout=2,
          autocommit=True
          )
  return vdgs_test
def refresh_flights_list():
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
  
def get_flishts_list():
  vdgs_test=vdgs_upload_connnection()
  if vdgs_test is None:
    return None   
  cur=vdgs_test.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  cur.execute("select * from flights_list_run;")
  data=cur.fetchall()
  cur.close
  vdgs_test.close()
  return dict([(str(x['flight_no']),x) for x in data])

def upload_lead_history():
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


def set_lead_cmd(flight,flt_type):
  conn=vdgs_local_connection()
  if conn is None:
    return
  cur = conn.cursor()
  cur.execute("INSERT INTO `VDGS`.`HY_VDGS_LeadCmd` VALUES(0,'VD0009','','%s','%s',0,0,0,0,2,now());"%(flight,flt_type))
  cur.close()
def get_work_state():
  conn=vdgs_local_connection()
  if conn is None:
    return None,None
  cur = conn.cursor()
  cur.execute("select * from HY_VDGS_LeadState;")
  data=cur.fetchone()
  cur.close()
  return data[4],ord(data[11]),data[15]

berth_state=0 #0空闲，1占用

def time_differ(time1,time2):
  time1=datetime.datetime.strptime(time1,"%H:%M")
  time2=datetime.datetime.strptime(time2,"%H:%M")
  dif_time=time1-time2
  return dif_time.total_seconds()/60

def read_flight_list():
  flight_list=[]
  try:
    with open('aaa.csv', 'rb') as f:
      dict_read=csv.DictReader(f)
      for row in dict_read:
        flight_list.append(row)
    return flight_list
  except Exception as e:
    print('Unable to save data to', 'flightlist.txt', ':', e)  
    return None

def get_flight_state(url,flt_type=1):
  try:
    print url
    driver = webdriver.PhantomJS()
    driver.get(url)
    data1=driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div/table/tbody/tr/td[2]/div/p')#操作频率过高  
    if data1:    
      print('访问过于频繁错误，休息50s之后继续访问')
      time.sleep(50)
      return None,None
    
    if flt_type==1:
      data2=driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[2]/i')#航班状态
    else:
      data2=driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[2]/i')
    if data2 :
      
      if  u'延误' == unicode(data2[0].text):
        state=3
      elif  u'到达' == unicode(data2[0].text): 
        state=2
      elif  u'计划' == unicode(data2[0].text): 
        state=0  
      elif  u'起飞' == unicode(data2[0].text): 
        state=1       
      elif u'取消' == unicode(data2[0].text):  
        state=4
    else :
      driver.close()
      return None,None
    if state == 1 :
      xpath= '//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[3]/p[2]' if flt_type==1 \
      else '//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[3]/p[2]'
      data3=driver.find_elements_by_xpath(xpath)
      if data3:
        driver.close()
        return 1,data3[0].text
      else :
        driver.close()
        return None,None
    else:
      driver.close()
      return state,None
  except Exception as e:
    
    print('can not get the url page :',  e)  
    return None,None
def get_new_arrive_flight( flist):
  date_today=time.strftime("%Y%m%d", time.localtime())
  for i, flt in enumerate(flist):      
    url='http://flights.ctrip.com/actualtime/fno--'+flt['flight_no']+'-'+date_today+'.html'
    pl_time=flt['pa_time']
    # pa_time=flt['parrival']
    time_now=time.strftime("%H:%M", time.localtime())
    if int(flt['state'])==0:
      if time_differ(time_now,pl_time)>30:
        state,atime=get_flight_state(url,int(flt['flt_type']))
        print(time_now,flt['flight_no'],flt['flt_type'],atime,state)
        time.sleep(30)
        if state==1 and atime and time_differ(atime,time_now)<15:
          
          set_lead_cmd(flt['flight_no'],flt['flt_type'])


          
def update_flights_state(flight,**kwargs):
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
#update_flights_state('SC1182',l_state=0)    
  
flight_list={} 
def main():
  global flight_list
  always_run=True
  isnewdayrun=True
  days_changed=False
  last_lead_state=0  #0空闲，1等待，
  while always_run:
    time_now=time.strftime("%H:%M", time.localtime())
    if time_differ(time_now,'05:00')>0 and time_differ(time_now,'05:05')<0:
      days_changed=True
    if days_changed and time_differ(time_now,'05:12')>0:
      days_changed=False
      isnewdayrun=True      
    if isnewdayrun:
      isnewdayrun=False
      refresh_flights_list()
      flight_list=get_flishts_list()
 
    flight,isleadcmd,leadstate=get_work_state()
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
    if not isleadcmd:
      flt_no,flt_type= vdgs_get_lead_cmd()
      if flt_type:
        set_lead_cmd(flt_no,flt_type)
        continue
    
    if not isleadcmd and flight_list:
      #get_new_arrive_flight(flight_list)
      date_today=time.strftime("%Y%m%d", time.localtime())
      for i, flt in flight_list.items():      
        url='http://flights.ctrip.com/actualtime/fno--'+flt['flight_no']+'-'+date_today+'.html'
        pl_time=flt['pa_time']
        # pa_time=flt['parrival']
        time_now=time.strftime("%H:%M", time.localtime())
        if int(flt['l_state'])==0:
          if time_differ(time_now,pl_time)>-30:
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
              update_flights_state(flt['flight_no'],w_state=state,desc_state="航班取消")
            elif state ==1:
              update_flights_state(flt['flight_no'],w_state=state,desc_state="已经起飞")            
            time.sleep(30)
      time.sleep(30)
    else:
      time.sleep(10)
  
  
if __name__=='__main__':
  main()
  
  if not 0:
    print 1111
  else :
    print 1000
  
  
  
  
  
  
  
  
  
  
  
  
  