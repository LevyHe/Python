#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:48:36 2017

@author: levy
"""

from six.moves import cPickle as pickle
import re,time,csv
from selenium import webdriver
import MySQLdb
import datetime

if 0 is not None :
  print '0 can print'

driver = webdriver.PhantomJS()

url='file:///home/levy/Desktop/flight/%E4%B8%AD%E5%9B%BD%E5%9B%BD%E9%99%85%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8CA1597%E8%88%AA%E7%8F%AD%E5%8A%A8%E6%80%81%E4%BF%A1%E6%81%AF-%E4%B8%AD%E5%9B%BD%E5%9B%BD%E9%99%85%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8CA1597%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2-%E6%90%BA%E7%A8%8B%E6%9C%BA%E7%A5%A8%E9%A2%84%E8%AE%A2.html'

#url='file:///home/levy/Desktop/flight/%E4%B8%AD%E5%9B%BD%E5%9B%BD%E9%99%85%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8CA1663%E8%88%AA%E7%8F%AD%E5%8A%A8%E6%80%81%E4%BF%A1%E6%81%AF-%E4%B8%AD%E5%9B%BD%E5%9B%BD%E9%99%85%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8CA1663%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2-%E6%90%BA%E7%A8%8B%E6%9C%BA%E7%A5%A8%E9%A2%84%E8%AE%A2.html'
#url='file:///home/levy/Desktop/flight/%E5%B1%B1%E4%B8%9C%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8SC4889%E8%88%AA%E7%8F%AD%E5%8A%A8%E6%80%81%E4%BF%A1%E6%81%AF-%E5%B1%B1%E4%B8%9C%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8SC4889%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2-%E6%90%BA%E7%A8%8B%E6%9C%BA%E7%A5%A8%E9%A2%84%E8%AE%A2.html'
url='file:///home/levy/Desktop/flight/GJGJ8867%E8%88%AA%E7%8F%AD%E5%8A%A8%E6%80%81%E4%BF%A1%E6%81%AF-GJGJ8867%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2-%E6%90%BA%E7%A8%8B%E6%9C%BA%E7%A5%A8%E9%A2%84%E8%AE%A2.html'
driver.get(url)

pal='//*[@id="base_bd"]/div/div[2]/div[2]/div[1]/div[1]/div[2]/i'
pal='//*[@id="base_bd"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/i'
pal='//*[@id="base_bd"]/div/div[2]/div/div[2]/div[1]/div[3]/p[2]'
data1=driver.find_elements_by_xpath(pal)
for i in data1:
  print i.text
  if  u'延误' == unicode(i.text):
    print '航班延误'
  elif  u'到达' == unicode(i.text): 
    print '航班到达'
  elif  u'计划' == unicode(i.text): 
    print '计划'

driver.quit()