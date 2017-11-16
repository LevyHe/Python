#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:21:54 2017

@author: levy
"""

#from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
from PIL import Image
import imghdr
import numpy as np

img_width, img_height = 200, 200
rescale=1. / 255
load_weights='/home/levy/MachineLearning/berth_detection/plane_weights.h5'

Model=None
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)
    

    


  
def plane_act(weights,input_shape):
  model = Sequential()
  model.add(Conv2D(32, (3, 3), input_shape=input_shape))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  
  model.add(Conv2D(32, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  
  model.add(Conv2D(64, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  
  model.add(Flatten())
  model.add(Dense(64))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(2))
  model.add(Activation('softmax'))
  
  
  model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
  if weights:
    model.load_weights(weights)
    
  return model


def InitModel():
  global Model
  if not os.path.exists(load_weights):
    raise ValueError('Failed to find file: ' + load_weights)
  else :
    Model=plane_act(load_weights,input_shape)

  

def load_image_from_string(string):
  if string is None:
    return None
  import StringIO
  #START_CUT_WIDTH=360
  #START_CUT_HIGHT=160
  IMAGE_SIZE=400  
  img_io_file=StringIO.StringIO(string)
  if imghdr.what(img_io_file) is None:
    return None
  im = Image.open(img_io_file) 
  if(im.size[0]>IMAGE_SIZE+160):
    OFFSET=[80,0]
  else :
    OFFSET=[0,0] 
  reshape=tuple(np.array(im.size)/2-IMAGE_SIZE/2-OFFSET)+tuple(np.array(im.size)/2+IMAGE_SIZE/2-OFFSET)  
  #reshape=(START_CUT_WIDTH,START_CUT_HIGHT,START_CUT_WIDTH+IMAGE_SIZE,START_CUT_HIGHT+IMAGE_SIZE)
  im=im.crop(reshape)# (left, upper, right, lower)
  im=im.resize((img_width, img_height),resample=Image.BICUBIC)
  frame=np.asarray(im,dtype=np.float)*rescale
  x=np.expand_dims(frame, axis=0)
  return x


def IsImageHasPlane(img):
  '''
  img is a string img buffer
  '''
  if Model is None:
    print ("Model is not init")
    return 
  model=Model
  
  x=load_image_from_string(img)
  if x is None:
    return None
  pre=model.predict(x)
  s=pre
  pre=np.argmax(pre,1)
  pre=pre.astype(np.int)
  return sum(pre),s

train_data_dir = '/media/levy/Project/linux/newplane/'
if __name__=="__main__":
  InitModel()
  plane_list=os.listdir(train_data_dir+'plane')
  none_list=os.listdir(train_data_dir+'none')
  
  for i in plane_list:
    im=os.path.join(train_data_dir+'plane',i)
    with open(im,'rb') as f:
      png=f.read()
      pre,s=IsImageHasPlane(png)
      if pre ==0 :
        print (i,pre,s)
  for i in none_list:
    im=os.path.join(train_data_dir+'none',i)
    with open(im,'rb') as f:
      png=f.read()
      pre,s=IsImageHasPlane(png)
      if pre ==1 :
        print (i,pre,s)


#START_CUT_WIDTH=160
#START_CUT_HIGHT=160
#IMAGE_SIZE=400
#im_arr=np.array(list(image_file))
#im_arr=map(ord,im_arr)


#if __name__=="__main__":
#
#  print "__file__=%s" % __file__
#  
#  print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
#  
#  print "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__))
#  
#  print ("os.path.split(os.path.realpath(__file__))=%s" % os.path.split(os.path.realpath(__file__))[0])
#  
#  print "os.path.abspath(__file__)=%s" % os.path.abspath(__file__)
#  
#  print ('os.getcwd()=%s' % os.getcwd())
#  
#  print ('sys.path[0]=%s'% sys.path[0])
#  
#  print ('sys.argv[0]=%s' % os.path.basename(sys.argv[0]))

#quit()
#class_list=['none','plane']
#InitModel()
#list_file=os.listdir("/home/levy/Desktop/666")
#for i in list_file:
#  im=os.path.join("/home/levy/Desktop/666",i)
#  with open(im,'rb') as f:
#    png=f.read()
#  pre=IsImageHasPlane(png)
#  os.rename(im,class_list[pre]+i)
##
#if __name__=='__main__':
#  class_list=['none','plane']
#  image_file = '/home/levy/MachineLearning/berth_detection/pysocket.py'
#  image_file='/home/levy/linux/DeepLearning/img/test/plane/plane1025.png'  
#  with open(image_file,'rb') as f:
#    png=f.read()
#  InitModel()
#  pre=IsImageHasPlane(png)
#  if pre is None:
#    print ("can not pre this file")
#  else :
#    print("pred file name is "+image_file+".result is "+class_list[pre])
  
#if __name__=='__main__':
#  import socket,time
#  InitModel()
#  count=0
#  server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#  if os.path.exists("/tmp/vdgs1012.sock"):
#    os.unlink("/tmp/vdgs1012.sock")
#  server.bind("/tmp/vdgs1012.sock")
#  server.listen(0)
#  always_run = True
#  while always_run:
#    print("top")
#    connection, address = server.accept()
#    print("down")
#    re=connection.recv(1024*1024*3)
#    pre=IsImageHasPlane(re)
#    if(pre is not None):
#      connection.sendall("vdgs:%d"% pre)
#      print ("can not delect the image")
#    else :
#      connection.sendall("vdgs:error")
#      continue
#   # class_list=['none','plane']
#    #connection.send("test: %d"%len( re))
#   # time.sleep(1)
#    count+=1
#    print("receive image has %d plane,num count=%d"%(pre,count))
#  connection.close()
#    
    





