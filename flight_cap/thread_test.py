#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:56:54 2017

@author: levy
"""

import threading,time
from selenium import webdriver


class AccessWeb(threading.Thread):
  '''thread access the web'''
  state=None
  atime=None
  active=None
  driver=None
  def __init__(self,url=None,f_type=1,driver=None):
    super(AccessWeb, self).__init__()
    if driver is None:
      self.driver = webdriver.PhantomJS()
      time.sleep(3)
      self.driver.set_page_load_timeout(20)
      self.driver.set_script_timeout(20)  
    else :
      self.driver=driver
    self.url=url
    self.f_type=f_type
    self.active=True
    pass
  def is_valid_date(self,str):
    '''判断是否是一个有效的时间字符串'''
    try:
      time.strptime(str, "%H:%M")
      return True
    except:
      return False
  def run(self):
    try:
      self.state=None
      self.atime=None
      self.driver.get(self.url)
      data1=self.driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div/table/tbody/tr/td[2]/div/p')#操作频率过高 
      if data1:
        return
      if self.f_type==1:
        data2=self.driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[2]/i')#航班状态
      else:
        data2=self.driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[2]/i')
        if not data2:
  	    data2=self.driver.find_elements_by_xpath('//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[2]/i')          
      if data2 :     
        if  u'延误' == unicode(data2[0].text):
          self.state=3
        elif  u'到达' == unicode(data2[0].text): 
          self.state=2
        elif  u'计划' == unicode(data2[0].text): 
          self.state=0  
        elif  u'起飞' == unicode(data2[0].text): 
          self.state=1       
        elif u'取消' == unicode(data2[0].text):  
          self.state=4      
      if self.state == 1 :
        xpath= '//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[3]/p[2]' if self.f_type==1 \
        else '//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[3]/p[2]'
        data3=self.driver.find_elements_by_xpath(xpath)
        print data3[0].text
        if self.is_valid_date(str(data3[0].text)):
          self.atime=data3[0].text
    except Exception as e:
      print('can not get the url page :',  e)  
      self.state=None
      self.atime=None
  def get_web_result(self):
    self.join(60)         #等待60s
    if self.isAlive():
      self.active=None
      self.driver=None
      return None,None
    else :
      return self.state,self.atime

wdriver=None

def get_flight_state(url,f_type):
  global wdriver 
  if wdriver is None :
    wdriver = webdriver.PhantomJS()
    time.sleep(3)
    wdriver.set_page_load_timeout(20)
    wdriver.set_script_timeout(20)
  thweb=AccessWeb(url,f_type,wdriver)
  thweb.setDaemon(True)
  thweb.start()
  state,atime=thweb.get_web_result()
  print (state,atime,url)
  if not thweb.active :
    wdriver = webdriver.PhantomJS()
    time.sleep(3)
    wdriver.set_page_load_timeout(20)
    wdriver.set_script_timeout(20)
  return state,atime
  
  
  
