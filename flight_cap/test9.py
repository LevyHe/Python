#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 09:20:21 2017

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
  try :
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
  except Exception as e:
    print('Unable  connect to 58.211.162.30  :', e)  
    return None

image_addr='/home/levy/MachineLearning/berth_detection/none0.png'
image_addr='/home/levy/MachineLearning/berth_detection/plane1222.jpg'

video_path='/media/levy/Project/Project/VDGS/record_fmt/04-02-092220.mp4'

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


server_addr=('192.168.1.96',5012)
def get_image_form_socket():
  try:
    import socket,string
    from select import select  
    clent_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    clent_fd.connect(server_addr)
    clent_fd.sendall("vdgs:image")
    header=clent_fd.recv(16)
    if header:
      reg=re.findall(r"\d+",header) 
      print(reg)
      image_size=string.atoi(reg[0])
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

if __name__=='__main__':
#  import random 
#  print random.choice([1,2,3,4])
  jpg= get_image_form_socket()
#  if jpg:
#    update_vdgs_state(image=jpg)
    #time.sleep(5)
   
   
   
   