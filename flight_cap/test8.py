#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:05:02 2017

@author: levy
"""

import os,time
from wifi import Cell, Scheme
from selenium import webdriver

interface='wlp110s0'
#
#net_state=os.system('ping 58.211.162.30  -c 2')
#if net_state:
#  print 'false'
#else:
#  print 'ok'
  
#pip=os.popen("route | grep default | grep %s | awk '{print $2}'"%interface,"r")
#print 
#pip.close()


#'nmcli device connect wlp110s0'
#'nmcli device disconnect wlp110s0'


def net_check_reconnect():
  try:
    driver = webdriver.PhantomJS()
    net_state=os.system('ping 58.211.162.31  -c 2')
    if not net_state:
      return True
    os.system('nmcli device disconnect %s'%interface)
    time.sleep(2)
    os.system('nmcli device connect %s'%interface)
    time.sleep(2)
    pip=os.popen("route | grep default | grep %s | awk '{print $2}'"%interface,"r")
    gw=pip.read()
    pip.close()
    os.system("route add default gw %s"%gw)
    
    driver.get('http://flights.ctrip.com/actualtime/arrive-weh/')
    driver.close()
    driver.quit()
  except Exception as e:
    print('Unable connect to server:', e)  
    
if __name__=='__main__':
  while True:
    net_check_reconnect()
    time.sleep(30)