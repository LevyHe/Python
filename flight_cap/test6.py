#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 16:37:15 2017

@author: levy
"""

from six.moves import cPickle as pickle
import re,time,csv
from selenium import webdriver
import MySQLdb
import datetime
import numpy as np

def vdgs_upload_connnection():
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

image_addr='/home/levy/MachineLearning/berth_detection/none0.png'
image_addr='/home/levy/MachineLearning/berth_detection/plane1222.jpg'

def update_vdgs_state(**kwargs):
  keys =','.join([str(k)+"=%s" for k in kwargs.keys()])
  print keys
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
import cv2  
def draw_text(frame, text, x, y, color=(0,0,255), thickness=2, size=1,):
        if x is not None and y is not None:
            cv2.putText(
                frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)  
  
#with open(image_addr ,'rb') as f:
#  image=f.read()
#
#  update_vdgs_state(image=image)#MySQLdb.Binary(image)
  
def pre_view_airport():
  
  vdgs_test=vdgs_upload_connnection()
  cur=vdgs_test.cursor()
  while True:
    cur.execute("select lead_state,run_count,image from vdgs_states_value limit 1;")
    data=cur.fetchone()
    lead_state,run_count,frame=data
    test_dis="lead_state=%s,run_count=%s"%(lead_state,run_count)
    if frame :
      frame =map(ord,frame)
      frame=np.array(frame).astype(np.uint8)
      #cv2.putText(frame,test_dis,(100, 100),cv2.FONT_HERSHEY_SIMPLEX,0.3,)
      frame=cv2.imdecode(frame,cv2.CV_LOAD_IMAGE_COLOR)
      draw_text(frame,test_dis,10,100)
      cv2.imshow("preview",frame)
    
    k=cv2.waitKey(10*1000)
    if (k & 0xff == ord('q')):  

      cv2.destroyAllWindows()
      break  
  cur.close()
  vdgs_test.close()
    
pre_view_airport()

#import os 
#for i in range(9,0,-1):
#  print i
#  new='test%d.log'%i
#  old='test%d.log'%(i-1)
#  if os.path.exists(old):
#    os.rename(old,new)

    
    
  














#os.rename()

  