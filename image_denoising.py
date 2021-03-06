# -*- coding: utf-8 -*-
"""Image_Denoising.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16Kwf0RogWbUq9jyByGXVZ836iItFyxCy

## Importing fashion dataset
"""

from keras.datasets import mnist

"""### Importing Libraries"""

import keras
from keras import callbacks
from keras.models import Model
from keras.optimizers import Adadelta
from keras.layers import Input, Conv2D, MaxPool2D, UpSampling2D

"""### Downloading and Preprocessing of dataset and adding some noise to it."""

import numpy as np

(train_X, train_y), (test_X, test_y) = mnist.load_data()

# to convert values from 0 to 255 into range 0 to 1.
train_X = train_X.astype('float32') / 255.
test_X = test_X.astype('float32') / 255.
train_X = np.reshape(train_X, (len(train_X), 28, 28, 1))  # adapt this if using `channels_first` image data format
test_X = np.reshape(test_X, (len(test_X), 28, 28, 1))  # adapt this if using `channels_first` image data format

noise_factor = 0.5
#np.random.normal => random means to obtain random samples and normal means normal or gaussian distribution, i.e. random sample from gaussian distribution
train_X_noisy = train_X + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=train_X.shape)  
test_X_noisy = test_X + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=test_X.shape) 

# to make values in the range of 0 to 1, if values < 0 then they will be equal to 0 and values > 1 then they will be equal to 1.
train_X_noisy = np.clip(train_X_noisy, 0., 1.)   
test_X_noisy = np.clip(test_X_noisy, 0., 1.)

"""## Let's visualize original and noisy images"""

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10))
for i in range(5):
  plt.subplot(1, 5, i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(train_X[i].reshape(28, 28), cmap='gray')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 10))
for i in range(5):
  plt.subplot(1, 5, i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(train_X_noisy[i].reshape(28, 28), cmap='gray')
plt.tight_layout()
plt.show()

"""#Defining our Image denoising autoencoder"""
Input_img = Input(shape=(28, 28, 1))  

#encoding architecture
x1 = Conv2D(64, (3, 3), activation='relu', padding='same')(Input_img)
x1 = MaxPool2D( (2, 2), padding='same')(x1)
x2 = Conv2D(32, (3, 3), activation='relu', padding='same')(x1)
x2 = MaxPool2D( (2, 2), padding='same')(x2)
x3 = Conv2D(16, (3, 3), activation='relu', padding='same')(x2)
encoded    = MaxPool2D( (2, 2), padding='same')(x3)

# decoding architecture
x3 = Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
x3 = UpSampling2D((2, 2))(x3)
x2 = Conv2D(32, (3, 3), activation='relu', padding='same')(x3)
x2 = UpSampling2D((2, 2))(x2)
x1 = Conv2D(64, (3, 3), activation='relu')(x2)
x1 = UpSampling2D((2, 2))(x1)
decoded   = Conv2D(1, (3, 3), padding='same')(x1)


autoencoder = Model(Input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

"""## Structure of our autoencoder"""

autoencoder.summary()

"""### Enabling Early Stopping"""

from keras.callbacks import EarlyStopping
early_stopper = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')

"""## Training our autoencoder and validating it on validation data"""

a_e = autoencoder.fit(train_X_noisy, train_X,
                epochs=100,
                batch_size=128,
                shuffle=True,
                validation_data=(test_X_noisy, test_X),
                callbacks=[early_stopper])

"""## Making Predictions"""

# to predict the reconstructed images for the original images...
pred = autoencoder.predict(test_X_noisy)

"""## Visualizing our results"""

plt.figure(figsize=(10,10))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.xticks([]) # to remove x-axis  the [] empty list indicates this
    plt.yticks([]) # to remove y-axis
    plt.grid(False) # to remove grid
    plt.imshow(test_X[i].reshape(28, 28), cmap='gray') #display the image 
plt.tight_layout() # to have a proper space in the subplots
plt.show()

plt.figure(figsize=(10,10))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.xticks([]) # to remove x-axis  the [] empty list indicates this
    plt.yticks([]) # to remove y-axis
    plt.grid(False) # to remove grid
    plt.imshow(test_X_noisy[i].reshape(28, 28), cmap='gray') #display the image 
plt.tight_layout() # to have a proper space in the subplots
plt.show()

# to visualize reconstructed images(output of autoencoder)
plt.figure(figsize=(10,10))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.xticks([]) # to remove x-axis  the [] empty list indicates this
    plt.yticks([]) # to remove y-axis
    plt.grid(False) # to remove grid
    plt.imshow(pred[i].reshape(28, 28), cmap='gray') #display the image 
plt.tight_layout() # to have a proper space in the subplots
plt.show()

