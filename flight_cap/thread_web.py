#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:06:33 2017

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
  flights={}
  url='http://www.airwh.com/hbsearch/searchlist.htm?page=1&city=&cityX=&flightNum=&status=%E8%BF%9B%E6%B8%AF'
  def __init__(self,url=None,f_type=1,driver=None):
    super(AccessWeb, self).__init__()
    if driver is None:
      self.driver = webdriver.PhantomJS()
      time.sleep(3)
      self.driver.set_page_load_timeout(20)
      self.driver.set_script_timeout(20)  
    else :
      self.driver=driver
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
  def unicode_stae(self,val):
    state=None
    try:
      if  u'延误' == unicode(val):
        state=3
      elif  u'到达' == unicode(val): 
        state=2
      elif  u'计划' == unicode(val): 
        state=0  
      elif  u'起飞' == unicode(val): 
        state=1       
      elif u'取消' == unicode(val):  
        state=4  
      else:
        state=0
      return state
    except:
      return None
  def try_int(self,val):
    try:
      return int(val)
    except:
      return None
  def run(self):
    try:
      self.driver.get(self.url)
      next_page_enable=True
      xpath='//*[@id="tslyAddForm"]/div/div/table/tbody/tr'
      while next_page_enable:
        data=self.driver.find_elements_by_xpath(xpath)
        for ii in data:
          hh=ii.find_elements_by_tag_name('td')
          l1=[]
          for jj in hh:
            l1.append((jj.get_attribute('innerText')))
          if len(l1)<12 or self.try_int(l1[3])!=1:
            continue
          self.flights[str(l1[0])]=l1
        page_span=wdriver.find_elements_by_xpath('//*[@id="kkpager"]/div[1]/span[1]/*')  
        for ii in page_span:
          if ii.text==u'下一页': 
            np_url=ii.get_attribute('href') 
            if np_url :
              time.sleep(4)
              self.driver.get(np_url)
              time.sleep(1)
              break
            else:
              next_page_enable=False        
    except Exception as e:
      print('can not get the url page :',  e)  
  def get_web_result(self):
    self.join(60)         #等待60s
    if self.isAlive():
      self.active=None
      self.driver=None
      return None
    else :
      return self.flights
   

wdriver=None

def get_flight_state():
  try:
    global wdriver 
    if wdriver is None :
      wdriver = webdriver.PhantomJS()
      time.sleep(3)
      wdriver.set_page_load_timeout(20)
      wdriver.set_script_timeout(20)
    thweb=AccessWeb(driver=wdriver)
    thweb.setDaemon(True)
    thweb.start()
    fls=thweb.get_web_result()
    if not thweb.active :
      wdriver = webdriver.PhantomJS()
      time.sleep(3)
      wdriver.set_page_load_timeout(20)
      wdriver.set_script_timeout(20)
    return fls
  except:
    return None

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  