#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 22:39:44 2017

@author: levy
"""

from six.moves import cPickle as pickle
import re,time,random
from selenium import webdriver
try:
  with open('flight.pickle', 'rb') as f:
   flight_list= pickle.load(f)
    
except Exception as e:
  print('Unable to open data to', 'flight.pickle', ':', e)
  
def check_if_same_flitgh(x,y):
  regx=re.findall('[A-Z]+|\d+',x)
  regy=re.findall('[A-Z]+|\d+',y)
  if regx[0]==regy[0] and(((int(regx[1])-1)==int(regy[1])) or ((int(regx[1])+1)==int(regy[1]))):
    return True
  else :
    return False  

count=0
try:
  driver = webdriver.PhantomJS()
  for i,flight in enumerate( flight_list):
    #reg=re.findall('[A-Z]+|\d+',flight['flight_l'])
    #print(i,flight['flight_l'],check_if_same_flitgh(flight['flight_l'],'SC1827'))
    if flight['ref1'] :
      driver.get(flight['ref1'])
      data=driver.find_elements_by_class_name('strong')
      if len(data)>3:
        berth=data[4].text
        flight['berth']=berth
      elif len(data)>1:
        berth=data[1].text
        flight['berth']=berth
      time.sleep(random.uniform(3,5))
#    if flight['ref2'] and not (flight['pleave'] and flight['parrival']):
#      driver.get(flight['ref2'])
#      data1=driver.find_elements_by_xpath("//div[@class='inl departure']/p[@class='gray']")
#      data2=driver.find_elements_by_xpath("//div[@class='inl arrive']/p[@class='gray']")
#      if data1 and data2:
#        pleave=data1[-1].text.split()[1]
#        parrvial=data2[-1].text.split()[1]
#        flight['pleave']=pleave
#        flight['parrival']=parrvial
#        flight_list[i]=flight
#      time.sleep(3)
    count+=1
    print(flight['flight_a'],flight['flight_l'],count)
    
except Exception as e:
  print('what error', ':', e)
  
    
#driver.get('http://flights.ctrip.com/actualtime/fno--sc1828.html?DPort=WEH&APort=PEK')
#data=driver.find_elements_by_class_name('strong')
#data=driver.find_elements_by_xpath("//div[@class='inl departure']/p[@class='gray']")
#data=driver.find_elements_by_xpath("//div[@class='inl arrive']/p[@class='gray']")
##berth=data[1]
#for i in data:
#  print(i.text.split()[1])
  
try:
  with open('flight.pickle', 'wb') as f:
    pickle.dump(flight_list, f, pickle.HIGHEST_PROTOCOL)
except Exception as e:
  print('Unable to save data to', 'flight.pickle', ':', e)
  
driver.quit()