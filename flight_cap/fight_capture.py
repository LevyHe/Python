#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 20:49:24 2017

@author: levy
"""

#import httplib2  
#import urllib2  
import re,time #正则表达式模块  
from selenium import webdriver
from six.moves import cPickle as pickle

#driver = webdriver.PhantomJS()
#driver.get('http://flights.ctrip.com/actualtime/arrivecity-aline-weh-ca/')
#data = driver.title
#print data
flight_list=[];
flight={'flight_l':None,'flight_a':None,'flt':None,'pleave':None,'parrival':None,'aleave':None,'aarrival':None,'berth':None,'ref1':None,'ref2':None}
#web_url='http://flights.ctrip.com/actualtime/depart-weh/'
#web_url1='http://flights.ctrip.com/actualtime/arrivecity-aline-weh-ca/'
#driver = webdriver.PhantomJS()
#driver.get(web_url)
#data = driver.find_elements_by_class_name("bg_0")
#
#data =driver.find_elements_by_xpath("//table[@class='dynamic_data']")
#data = driver.find_elements_by_link_text('查看')
#for i in data:
#  #print(i.target)
#  #li=i.text.split()[0]
#  print(i.,i.get_attribute('href'))
#driver.quit()

def check_if_same_flitgh(x,y):
  regx=re.findall('[A-Z]+|\d+',x)
  regy=re.findall('[A-Z]+|\d+',y)
  if regx[0]==regy[0] and(((int(regx[1])-1)==int(regy[1])) or ((int(regx[1])+1)==int(regy[1]))):
    return True
  else :
    return False  

web_list=['http://flights.ctrip.com/actualtime/depart-weh/',
          'http://flights.ctrip.com/actualtime/depart-weh.p2/',
          'http://flights.ctrip.com/actualtime/depart-weh.p3/']
web_list_a=['http://flights.ctrip.com/actualtime/arrive-weh/',
            'http://flights.ctrip.com/actualtime/arrive-weh.p2/',
            'http://flights.ctrip.com/actualtime/arrive-weh.p3/']

driver = webdriver.PhantomJS()
for url in web_list:
  driver.get(url)
  data = driver.find_elements_by_link_text('查看')
  for e in data:
    dt=flight.copy()
    dt['flight_l']=e.get_attribute('title')
    dt['ref1']=e.get_attribute('href')
    flight_list.append(dt)
  print(len(flight_list))
  time.sleep(2)
  
  
for url in web_list_a:
  driver.get(url)
  data = driver.find_elements_by_link_text('查看')
  for e in data:
    dt=flight.copy()
    f_a=e.get_attribute('title')
    for i,fli in enumerate(flight_list):
      if check_if_same_flitgh(f_a,fli['flight_l']):
        fli['flight_a']=f_a
        fli['ref2']=e.get_attribute('href')
        flight_list[i]=fli
        break
  time.sleep(2)    
  
try:
  with open('flight.pickle', 'wb') as f:
    pickle.dump(flight_list, f, pickle.HIGHEST_PROTOCOL)
except Exception as e:
  print('Unable to save data to', 'flight.pickle', ':', e)

driver.quit()