#!/home/levy/apps/tensorflow/bin/python2
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
    
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf
config = tf.ConfigProto(device_count={"CPU": 2}, # limit to num_cpu_core CPU usage  
                inter_op_parallelism_threads = 1,   
                intra_op_parallelism_threads = 1,  
                log_device_placement=True)  

KTF.set_session(tf.Session(config = config))        

  
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
  print(pre)
  pre=np.argmax(pre,1)
  pre=pre.astype(np.int)
  print (model.outputs)
  return sum(pre)

def main():
  import socket,string,re
  from select import select  
  #import time
  InitModel()
  count=0
  server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  if os.path.exists("/tmp/vdgs1012.sock"):
    os.unlink("/tmp/vdgs1012.sock")
  server.bind("/tmp/vdgs1012.sock")
  server.listen(0)
  always_run = True
  while always_run:
    print("top")
    connection, address = server.accept()
    print("down")
   # image_size=connection.recv(8)
    header=connection.recv(16)
    if header:
      print(header)
      reg=re.findall(r"\d+",header) 
      print(reg)
      image_size=string.atoi(reg[0])
      recv_size=0
      image_buf=b""
      input_list = [connection]     
      while recv_size<image_size:
        iobj,_,_=select(input_list,[],[],1)
        if iobj is None:
          break
        image_data=connection.recv(1024)
        recv_size+=len(image_data)
        image_buf+=image_data
    else :
      continue
    if recv_size<image_size:
      connection.sendall("vdgs:error")
      continue
    pre=IsImageHasPlane(image_buf)
    if(pre is not None):
      connection.sendall("vdgs:%d"% pre)
      #print ("can not delect the image")
      count+=1
    else :
      connection.sendall("vdgs:error")
      continue
     # class_list=['none','plane']
    #connection.send("test: %d"%len( re))
     # time.sleep(1)
    print("receive image has %d plane,num count=%d"%(pre,count))
  connection.close()


if __name__=='__main__':
  main()
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
  






