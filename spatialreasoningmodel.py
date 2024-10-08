# -*- coding: utf-8 -*-
"""SpatialReasoningModel (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b3pnG5tP32LqoFzpPH0iQY6QEKeYRa5g
"""

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import cifar10,cifar100

# example of loading the mnist dataset
from numpy import mean
from numpy import std
from sklearn import datasets
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten, BatchNormalization
from tensorflow.keras.optimizers import SGD
import tensorflow as tf

from tensorflow.keras.utils import to_categorical
#from tensorflow.keras.datasets import cifar10,cifar100
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import keras
import numpy as np
def conc(*inp1):
  return layers.Concatenate()(inp1)

def edim(inp,axis=-1):
    return tf.expand_dims(inp,axis)

import math

#!pip install tensorflow_addons
import tensorflow_addons as tfa

def mpool(psize,strides=2):
  return MaxPooling2D(pool_size=psize,strides=strides,padding="SAME")

def apool(psize,strides=None):
  if(strides is None):
    return AveragePooling2D(pool_size=psize,padding="SAME")
  else:
    return AveragePooling2D(pool_size=psize,strides=strides,padding="SAME")

def ln():
  return layers.LayerNormalization()

def bn():
  return layers.BatchNormalization()

def dense(size,act='relu'):
  return Dense(size,activation=act)

from keras.callbacks import ModelCheckpoint
import tensorflow.keras.layers as layers
filepath = 'my_best_model.hdf5'

def bnconv(inp,units,kernel_size):
  return BatchNormalization()(Conv2D(units,kernel_size,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0005))(inp))

def dense(units,act='relu'):
  return layers.Dense(units,activation=act)

def edim(inp,axis=-1):
    return tf.expand_dims(inp,axis)

def conv(inp,units,kernel_size):
  return Conv2D(kernel_size,units,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0005))(inp)

def cutout(image,size):
  return tfa.image.cutout(image,mask_size=(size,size))

def LaplacianFilter(input_tensor):
  filter = tf.constant([[[0.0,-1.0,0.0],[-1.0,4.0,-1.0],[0.0,-1.0,0.0]]])   #The filters for derivatives Cx, Cy ,[[0.0,-1.0],[1.0,0.0]]
  filter = filter[:,:,:,tf.newaxis]
  filter = tf.transpose(filter,[1,2,0,3])
  print(filter.shape)
  tf.print(filter[:,:,1,1])
  out = tf.nn.conv2d(input_tensor,filters=filter,padding="SAME",strides=[1, 1, 1, 1])  #basic convolution operation in tensorflow, the derivative filters are applied with stride 3
  return out


def LocalCurvature(input_tensor,scale=1,edge=True):
  filter = tf.constant([[[-1.0,0.0],[0.0,0.0]],[[1.0,0.0],[1.0,-1.0]]])   #The filters for derivatives Cx, Cy ,[[0.0,-1.0],[1.0,0.0]]
  filter = tf.transpose(filter,[1,2,0])
  filter = filter[:,:,tf.newaxis] #Expanding according to number of input channels
  filter = tf.tile(filter,[1,1,input_tensor.shape[-1],1])
  filter2 = tf.constant([[[0.0,0.0],[0.0,0.0]],[[1.0,0.0],[0.0,1.0]]])   #The filters for derivatives Cx, Cy ,[[0.0,1.0],[0.0,0.0]]
  filter2 = tf.transpose(filter2,[1,2,0])

  filter2 = filter2[:,:,tf.newaxis]
  filter2 = tf.tile(filter2,[1,1,input_tensor.shape[-1],1])                                         #Expanding according to number of input channels
  filter3 = tf.constant([[[1.0,0.0],[0.0,0.0]],[[0.0,0.0],[1.0,0.0]]])   #The filters for derivatives Cx, Cy ,[[0.0,0.0],[1.0,0.0]
  filter3 = tf.transpose(filter3,[1,2,0])
  filter3 = filter3[:,:,tf.newaxis]
  filter3 = tf.tile(filter3,[1,1,input_tensor.shape[-1],1])
  out2 = tf.nn.conv2d(input_tensor, filters=filter2,padding="SAME",dilations=scale,strides=[1, 1, 1, 1])
  out3 = tf.nn.conv2d(input_tensor, filters=filter3,padding="SAME",dilations=scale,strides=[1, 1, 1, 1])
  out = tf.math.abs(tf.nn.conv2d(input_tensor,filters=filter,dilations=scale,padding="SAME",strides=[1, 1, 1, 1]))  #basic convolution operation in tensorflow, the derivative filters are applied with stride 3
  if edge:
    return tf.where(tf.abs(out2*out3)>0,out,0.0)
  else:
    return out

import tensorflow_datasets as tfds
import numpy as np

def preprocess_imagecont(image, label,image_size=32):
  image = tf.convert_to_tensor(image)
  image = tf.image.resize(image, [image_size,image_size])
  image1 = tfa.image.gaussian_filter2d(image, (2,2),3)
  image = tf.cast(image, tf.float32)
  #image = image/255.0
  positionsx1 = tf.range(start=0, limit=image_size, delta=float(1),dtype=tf.float32)
  positionsy1 = tf.range(start=0, limit=image_size, delta=float(1),dtype=tf.float32)
  positionsx1 = tf.expand_dims(tf.tile(tf.expand_dims(positionsx1,0),[image_size,1]),-1)
  positionsy1 = tf.expand_dims(tf.tile(tf.transpose(tf.expand_dims(positionsy1,0)),[1,image_size]),-1)
  positions11 = tf.concat([positionsx1,positionsy1],-1); positions11 = tf.tile(positions11[tf.newaxis,:,:,:],[image.shape[0],1,1,1])
  u = tf.image.sobel_edges(image1)
  angle = tf.where(u[:,:,:,0,0]!=0,tf.atan2(u[:,:,:,0,1],u[:,:,:,0,0]),0)
  angle = angle[:,:,:,tf.newaxis]

  image = tf.concat([image,angle/3.14,positions11],-1)
  #image = tf.concat([u[tf.newaxis,:,:,:],angle,positions11[tf.newaxis,:]],-1)
  #image=tf.squeeze(image,0)
  return image, label

labeled_batch_size=75
num_epochs = 60
batch_size = 30  # Corresponds to 200 steps per epoch
width = 32
temperature = 1
learning_rate=0.0001
#lr_drop=20


import keras.backend as K
image_size=28

import math

'''
Regular 2 Layer CNN model
'''

def ConvolutionalModel2Lyr(image_size=28,classes=10):
  inputs = layers.Input(shape=(image_size, image_size, 4))
  angle = inputs[:,:,:,1]; angle = tf.where(angle==1.0005072,0.0,angle); angle = tf.expand_dims(angle,-1)
  x1 = tf.tile(angle,[1,1,1,1])
  xc = LocalCurvature(x1)
  xc2 = LocalCurvature(xc)
  pos = inputs[:,:,:,2:]
  inputsi = inputs[:,:,:,0:1];
  f = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=64,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(inputsi))
  l1 = apool(2,strides=2)(f)
  l1 = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=100,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l1))
  l1 = mpool(2,strides=2)(f)
  l = layers.Flatten()(l1)
  l = layers.Dense(2048,activation='relu',kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l)
  x = layers.Dense(classes,activation='softmax')(l)
  return tf.keras.Model(inputs = inputs,outputs = x)

'''
Regular 4 Layer CNN model
'''

def ConvolutionalModel(image_size=28,classes=10):
  inputs = layers.Input(shape=(image_size, image_size, 4))
  angle = inputs[:,:,:,1]; angle = tf.where(angle==1.0005072,0.0,angle); angle = tf.expand_dims(angle,-1)
  x1 = tf.tile(angle,[1,1,1,1])
  xc = LocalCurvature(x1)
  xc2 = LocalCurvature(xc)
  pos = inputs[:,:,:,2:]
  inputsi = inputs[:,:,:,0:1];
  f = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=64,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(inputsi))
  l1 = apool(2,strides=2)(f)
  l1 = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=100,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l1))
  l1 = mpool(2,strides=2)(f)
  l1 = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=200,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l1))
  l1 = mpool(2,strides=2)(l1)
  l1 = bn()(layers.Conv2D(kernel_size=3,activation='relu',filters=256,kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l1))
  l1 = mpool(2,strides=2)(l1)
  l = layers.Flatten()(l1)
  l = layers.Dense(2048,activation='relu',kernel_initializer='glorot_normal',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l)
  x = layers.Dense(classes,activation='softmax')(l)
  return tf.keras.Model(inputs = inputs,outputs = x)

'''Multi-scale convolutional layer to learn scale invariant representation. This layer convolves the input with the filter at multiple scales and takes the
maxima of the outputs to pool the output across scales.'''

class MultiScaleConv(keras.layers.Layer):
  def __init__(self,kernel_size,regularizer=1,filters=256):
    self.kernel_size = kernel_size
    self.filters = filters
    self.regularizer=regularizer
    super(MultiScaleConv,self).__init__()

  def build(self, input_shape):
        shape = list(self.kernel_size) + [input_shape[-1], self.filters]
        if self.regularizer is not None:
            self.kernel = self.add_weight(name='kernel', shape=shape,
                                          initializer='glorot_normal',regularizer=tf.keras.regularizers.L2(0.0004),
                                         trainable=True)
        else:
            self.kernel = self.add_weight(name='kernel', shape=shape,
                                          initializer='glorot_uniform',trainable=True)
        super(MultiScaleConv, self).build(input_shape)

  def call(self,inputs):
    dup_cols=self.kernel
    l = layers.Maximum()([tf.nn.atrous_conv2d(inputs,rate=1,filters=dup_cols,padding="SAME"),tf.nn.atrous_conv2d(inputs,rate=2,filters=dup_cols,padding="SAME")])
    l = tf.keras.activations.relu(l)
    return l

'''The Spatial Reasoning Layer. This layer takes the scale or rotation invariant CNN features and assigns them to parts.
It then learns the spatial relations between these parts by firstly finding their location of maximum activation (through the argmax operation)
and then creating a matrix of pairwise distances between these parts using the found locations.'''
class SpatialReasoningLayer(keras.layers.Layer):
    def __init__(self, units=256, k=200,size=4,strides=4,**kwargs):
        super(SpatialReasoningLayer, self).__init__(**kwargs)
        self.k = k; self.bn = layers.BatchNormalization();
        self.units=units;self.size=size;self.strides=strides

    def build(self, input_shape):
#         print(input_shape)
#         print(self.units)
        self.weight = self.add_weight(name='w',
                                  shape=([self.units//self.k,self.k]),
                                  initializer='he_normal',
                                  regularizer=tf.keras.regularizers.L2(0.0005),
                                  trainable=True)
        self.wb = self.add_weight(name='wb',
                                  shape=([self.units//self.k]),
                                  initializer='he_normal',
                                  trainable=True)
        self.wd = self.add_weight(name='wd',
                                  shape=([self.units//self.k,self.k,self.k]),
                                  initializer='he_normal',
                                  trainable=True,
                                regularizer=tf.keras.regularizers.L2(0.00045))
        self.wdb = self.add_weight(name='wdb',
                                  shape=([self.units//self.k]),
                                  initializer='he_normal',
                                  trainable=True)


    def call(self,inputs):
        x = layers.GlobalMaxPooling2D()(inputs)
        fx = tf.argmax(tf.reduce_max(inputs,1),1)              #Location of Maximum activation along X-axis
        fy = tf.argmax(tf.reduce_max(inputs,2),1)              #Location of Maximum activation along Y-axis
        fx = tf.reshape(fx,[-1,fx.shape[1]//self.k,self.k]); fy = tf.reshape(fy,[-1,fy.shape[1]//self.k,self.k])
        fx_diff = (tf.subtract(fx[:,:,tf.newaxis,:],fx[:,:,:,tf.newaxis])) #Compute difference between x-coordinates of parts
        fy_diff = (tf.subtract(fy[:,:,tf.newaxis,:],fy[:,:,:,tf.newaxis])) #Compute difference between y-coordinates of parts
        fx_diff = tf.cast(fx_diff,tf.float32); fy_diff = tf.cast(fy_diff,tf.float32)

        distances = (tf.sqrt(tf.square(fx_diff) + tf.square(fy_diff))) # Compute euclidean distance
        distances = self.wd*distances                                  #Pass through a linear layer to learn weighted combination of distances
        spatial = tf.keras.activations.sigmoid(-(tf.reduce_sum(distances,[-1,-2])-self.wdb)**2)
        return x,spatial

'''
Single Layer Spatial Reasoning Model
'''
def SpatialRelationsModel(image_size=28,classes=10):
  inputs = layers.Input(shape=(image_size, image_size, 4))
  angle = inputs[:,:,:,1]; angle = tf.where(angle==1.0005072,0.0,angle); angle = tf.expand_dims(angle,-1)
  x1 = tf.tile(angle,[1,1,1,2])
  xc = LocalCurvature(x1,edge=True); xc = edim(tf.reduce_sum(xc,-1))
  xc2 = LocalCurvature(xc,edge=True); xc2 = edim(tf.reduce_sum(xc2,-1))
  pos = inputs[:,:,:,2:]
  inputsi = inputs[:,:,:,0:1]

  l = bn()(MultiScaleConv(filters=130,kernel_size=(3,3))(conc(inputsi)))
  l = mpool(2,strides=2)(l)
  l = layers.Dense(740,activation='relu')(l)
  l = bn()(layers.Dense(1240,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l))

  lc,sp = SpatialReasoningLayer(1240,8)(l)
  l = layers.Dense(3048,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(layers.Concatenate()([lc,sp]))
  x = layers.Dense(classes,activation='softmax')(l)
  return tf.keras.Model(inputs = inputs,outputs = x), tf.keras.Model(inputs = inputs,outputs = l)

'''
2 Layer Spatial Reasoning Model
'''

def SpatialRelationsModel2Lyr(image_size=28,classes=10):
  inputs = layers.Input(shape=(image_size, image_size, 4))
  angle = inputs[:,:,:,1]; angle = tf.where(angle==1.0005072,0.0,angle); angle = tf.expand_dims(angle,-1)
  x1 = tf.tile(angle,[1,1,1,2])
  xc = LocalCurvature(x1,edge=True); xc = edim(tf.reduce_sum(xc,-1))
  xc2 = LocalCurvature(xc,edge=True); xc2 = edim(tf.reduce_sum(xc2,-1))
  pos = inputs[:,:,:,2:]
  inputsi = inputs[:,:,:,0:1]

  l = bn()(MultiScaleConv(filters=130,kernel_size=(3,3))(conc(inputsi)))
  l = mpool(2,strides=2)(l)
  l = bn()(MultiScaleConv(filters=130,kernel_size=(3,3))(conc(inputsi)))
  l = mpool(2,strides=2)(l)
  l = layers.Dense(740,activation='relu')(l)
  l = bn()(layers.Dense(1240,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(l))

  lc,sp = SpatialReasoningLayer(1240,8)(l)
  l = layers.Dense(3048,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.0004))(layers.Concatenate()([lc,sp]))
  x = layers.Dense(classes,activation='softmax')(l)
  return tf.keras.Model(inputs = inputs,outputs = x), tf.keras.Model(inputs = inputs,outputs = l)