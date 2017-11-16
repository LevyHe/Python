#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:41:22 2017

@author: levy
"""

import socket
#import os

if __name__ == '__main__':
  client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  client.connect("/tmp/vdgs1012.sock")
  image_file = '/home/levy/MachineLearning/berth_detection/plane1222.jpg'
 # image_file='/home/levy/linux/DeepLearning/img/test/plane/plane1025.png'  
  with open(image_file,'rb') as f:
    png=f.read()

    #instr = raw_input()
    #instr="5"*5
    client.send(png)
    print client.recv(20)

    client.close()