#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:37:56 2017

@author: levy
"""

from six.moves import cPickle as pickle
import re,time,csv
from selenium import webdriver
import MySQLdb
import datetime

driver = webdriver.PhantomJS()
vdgs_local_info={
        'host':'localhost',
        'port' : 3306,
        'user':'vdgs',
        'passwd':'vdgs',
        'db' :'VDGS'}
#conn= MySQLdb.connect(
#        host='localhost',
#        port = 3306,
#        user='vdgs',
#        passwd='vdgs',
#        db ='VDGS',
#        )

vdgs_test=MySQLdb.connect(
        host='58.211.162.30',
        port = 3306,
        user='vdgs',
        passwd='vdgs_20171121',
        db ='vdgs_test',
        )
def vdgs_local_connection():
  conn= MySQLdb.connect(
          host='localhost',
          port = 3306,
          user='vdgs',
          passwd='vdgs',
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
#flight_list= read_flight_list()
#cur = vdgs_upload_connnection().cursor()
#try :
#  for f in flight_list:
#    sql="replace into flights_list values('"+f['flight_a']+"','"+f['flt']+"','"+f['pleave']+"','"+f['parrival']+"','','',0,0,"+str(f['type'])+",'未执行'"+");"
#    cur.execute(sql)
#except Exception as e:
#  print('Unable to save data to', 'flightlist.txt', ':', e)  
def refresh_flights_list():
  vdgs_test=vdgs_upload_connnection()
  if vdgs_test is None:
    return
  sql = '''delete from flights_list_run;
  insert into flights_list_run(`flight_no`,`flt_type`,`pd_time`,`pa_time`,`aa_time`,`ad_time`,`w_state`,`l_state`,`desc_state`,`update_time`)
  select *,now() from flights_list;'''
  cur = vdgs_test.cursor()
  cur.execute(sql)
  cur.close()
  vdgs_test.close()

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
#upload_lead_history()

#refresh_flights_list()
def get_flishts_list():
  vdgs_test=vdgs_upload_connnection()
  if vdgs_test is None:
    return None   
  cur=vdgs_test.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  cur.execute("select * from flights_list_run;")
  data=cur.fetchall()
  cur.close
  vdgs_test.close()
  print enumerate(data)
  return dict([(str(x['flight_no']),x) for x in data])
flights_run=get_flishts_list()
#for k,v in flights_run.items():
#  print(k,v)

for i, flt in enumerate(flights_run):      
   print i
   print flt




