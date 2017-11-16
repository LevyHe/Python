#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 18:42:07 2017

@author: levy
"""

from six.moves import cPickle as pickle
import re,time,csv
from selenium import webdriver
import MySQLdb
import datetime
import numpy as np
import cv2  


CV_CAP_PROP_POS_MSEC=0
CV_CAP_PROP_POS_FRAMES=1
CV_CAP_PROP_FRAME_COUNT=7
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

image_addr='/home/levy/MachineLearning/berth_detection/none0.png'
image_addr='/home/levy/MachineLearning/berth_detection/plane1222.jpg'

video_path='/media/levy/Project/Project/VDGS/record_fmt/04-02-092220.mp4'

def vdgs_get_lead_cmd():
  try:
    vdgs_test=vdgs_upload_connnection()
    cur=vdgs_test.cursor()
    cur.execute("select * from flights_lead_cmd limit 1;")
    data=cur.fetchone()
    
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
def upload_video_image_test():
  cap=cv2.VideoCapture(video_path) 
  grabbed, frame = cap.read()
  i=0
  frames_sum=cap.get(CV_CAP_PROP_FRAME_COUNT)
  while(grabbed):
    
    if frame is not None :
      #imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
      r,jpg = cv2.imencode(".jpg",frame)
      if r:
        update_vdgs_state(image=jpg.tostring())
        
      
      
    i+=5*30
    if(i<frames_sum):
        cap.set(CV_CAP_PROP_POS_FRAMES,i)   
    else:
        break
    print i
    grabbed, frame = cap.read()
    k=cv2.waitKey(5*1000)
    if (k & 0xff == ord('q')):  
      break
  cap.release()
if __name__=='__main__':
 print( vdgs_get_lead_cmd())