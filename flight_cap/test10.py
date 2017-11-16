#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 18:48:26 2017

@author: levy
"""

import cv2,os
from selenium import webdriver
import MySQLdb
import numpy as np

noplane_range=range(5388,5467)
noplane_range+=range(5537,5556)
plane_range=range(5467,5537)

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
image_dir='/media/levy/Project/linux/newplane'


CV_CAP_PROP_POS_MSEC=0
CV_CAP_PROP_POS_FRAMES=1
CV_CAP_PROP_FRAME_COUNT=7

START_CUT_WIDTH=360
START_CUT_HIGHT=160
IMAGE_SIZE=400  
def image_save(name,id_num):
  vdgs_test=vdgs_upload_connnection()
  if vdgs_test is None:
    return 
  cur=vdgs_test.cursor()
  cur.execute("select image from vdgs_states_history where id=%d limit 1;"%id_num)
  data=cur.fetchone()  
  cur.close()
  vdgs_test.close()
  if data:
    frame=data[0]
    frame =map(ord,frame)
    frame=np.array(frame).astype(np.uint8)
    frame=cv2.imdecode(frame,cv2.CV_LOAD_IMAGE_COLOR)
    frame=frame[START_CUT_HIGHT:START_CUT_HIGHT+IMAGE_SIZE,START_CUT_WIDTH:START_CUT_WIDTH+IMAGE_SIZE,:]
    image_file=os.path.join(image_dir,name,name+str(id_num)+'.jpg')
    cv2.imwrite(image_file,frame)   
    
for i in    noplane_range:
  print i
  image_save('none',i)
for i in    plane_range:
  print i
  image_save('plane',i)    
    