#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:24:34 2017

@author: levy
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 19:00:37 2017

@author: levy
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os

# dimensions of our images.
img_width, img_height = 200, 200

train_data_dir = '/media/levy/Project/linux/newplane/'
validation_data_dir = '/media/levy/Project/linux/valid_re/'
load_weights='plane_weights.h5'

nb_train_samples = 168
nb_validation_samples = 2168
epochs = 4
batch_size = 16



if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

Model=None
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

 
def plane_new_tarin():
  global Model
  InitModel()
  # this is the augmentation configuration we will use for training
  train_datagen = ImageDataGenerator(
      rescale=1. / 255,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True)
  
  # this is the augmentation configuration we will use for testing:
  # only rescaling
  test_datagen = ImageDataGenerator(rescale=1. / 255)
  
  train_generator = train_datagen.flow_from_directory(
      train_data_dir,
      target_size=(img_width, img_height),
      batch_size=batch_size,
      #class_mode='binary'
      )
  
  validation_generator = test_datagen.flow_from_directory(
      validation_data_dir,
      target_size=(img_width, img_height),
      batch_size=batch_size,
      #class_mode='binary'
      )
  
  Model.fit_generator(
      train_generator,
      steps_per_epoch=nb_train_samples // batch_size,
      epochs=epochs,
      validation_data=validation_generator,
      validation_steps=nb_validation_samples // batch_size)
#  Model.save_weights(load_weights)

plane_new_tarin()






















