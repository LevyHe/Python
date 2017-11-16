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

driver = webdriver.PhantomJS()
conn= MySQLdb.connect(
        host='192.168.1.96',
        port = 3306,
        user='vdgs',
        passwd='vdgs20161121',
        db ='VDGS',
        connect_timeout=20,
        )

def set_lead_cmd(flight,flt_type):
  cur = conn.cursor()
  cur.execute("INSERT INTO `VDGS`.`HY_VDGS_LeadCmd` VALUES(0,'VD0009','','%s','%s',0,0,0,0,2,now());"%(flight,flt_type))
  cur.close()
def get_work_state():
  cur = conn.cursor()
  cur.execute("select * from HY_VDGS_LeadState;")
  data=cur.fetchone()
  cur.close()
  return ord(data[11]),data[15]

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
    return None,None
  if state == 1 :
    xpath= '//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[3]/p[2]' if flt_type==1 \
    else '//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[3]/p[2]'
    data3=driver.find_elements_by_xpath(xpath)
    if data3:
      return 1,data3[0].text
    else :
      return None,None
  elif state in [0,3]:
    return 0,None
  elif state in [2,4]:
    return 2,None

  driver.quit()

def get_new_arrive_flight( flist):
  date_today=time.strftime("%Y%m%d", time.localtime())
  for i, flt in enumerate(flist):      
    url='http://flights.ctrip.com/actualtime/fno--'+flt['flight_a']+'-'+date_today+'.html'
    pl_time=flt['pleave']
    # pa_time=flt['parrival']
    time_now=time.strftime("%H:%M", time.localtime())
    if int(flt['state'])==0:
      if time_differ(time_now,pl_time)>30:
        state,atime=get_flight_state(url,int(flt['type']))
        print(time_now,flt['flight_a'],flt['flt'],atime,state)
        time.sleep(30)
        if state==1 and atime and time_differ(atime,time_now)<15:
          
          set_lead_cmd(flt['flight_a'],flt['flt'])
          flt['state']=1
          flist[i]=flt
        elif state==2:
          flt['state']=2
          flist[i]=flt
          

  
  
def main():
  always_run=True
  isnewdayrun=True
  days_changed=False
  
  while always_run:
    time_now=time.strftime("%H:%M", time.localtime())
    if time_differ(time_now,'05:00')>0 and time_differ(time_now,'05:30')<0:
      days_changed=True
    if days_changed and time_differ(time_now,'06:00')>0:
      days_changed=False
      isnewdayrun=True
      
    if isnewdayrun:
      isnewdayrun=False
      flight_list=read_flight_list()
 
    isleadcmd,leadstats=get_work_state()  
    if not isleadcmd and flight_list:
      get_new_arrive_flight(flight_list)
      
      time.sleep(30)
    else:
      time.sleep(10)
  
  
if __name__=='__main__':
  main()
  
  
  
  
  
  
  
  
  
  
  
  
  