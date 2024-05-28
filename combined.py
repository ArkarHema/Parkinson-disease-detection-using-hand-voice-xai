# -*- coding: utf-8 -*-
"""combined.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z1uS14QOVUJocYkiL30q4PvzKhRFGlY0
"""

import keras
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Flatten
from keras import optimizers
from keras.models import Sequential
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   validation_split=0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255,
                                shear_range = 0.2,
                                   zoom_range = 0.2,
                                   validation_split=0.2,
                                   horizontal_flip = True)


training_set = train_datagen.flow_from_directory(r'/content/drive/MyDrive/park/spiral/training',
                                                 target_size = (224, 224),
                                                 batch_size = 8,
                                                 subset="training",
                                                 class_mode = 'categorical')

validation_set = train_datagen.flow_from_directory(r'/content/drive/MyDrive/park/spiral/testing',
                                                 target_size = (224, 224),
                                                 batch_size = 8,
                                                subset="validation",
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(r'/content/drive/MyDrive/park/spiral/testing',
                                            target_size = (224, 224),
                                            batch_size = 8,
                                            class_mode = 'categorical')

#color_mode = "grayscale"


STEP_SIZE_TRAIN=training_set.n//training_set.batch_size
STEP_SIZE_VALID=validation_set.n//validation_set.batch_size
STEP_SIZE_TEST=test_set.n//test_set.batch_size

from google.colab import drive
drive.mount('/content/drive')

print(STEP_SIZE_TRAIN)
print(STEP_SIZE_TEST)

training_set

IMAGE_SIZE = [224, 224]
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
#here [3] denotes for RGB images(3 channels)

#don't train existing weights
for layer in vgg.layers:
 layer.trainable = False

x = Flatten()(vgg.output)
prediction = Dense(2, activation='sigmoid')(x)
model = Model(inputs=vgg.input, outputs=prediction)
model.compile(loss='binary_crossentropy',
                    optimizer=optimizers.Adam(),
                    metrics=['accuracy'])
model.summary()

from datetime import datetime
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras.callbacks import ReduceLROnPlateau
lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1),
                               cooldown=0,
                               patience=5,
                               min_lr=0.5e-6)
checkpoint = ModelCheckpoint(filepath='mymodel.h5',
                               verbose=1, save_best_only=True)
callbacks = [checkpoint, lr_reducer]
start = datetime.now()
history = model.fit(training_set,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    epochs = 18, verbose=5,
                    validation_data = validation_set,
                    validation_steps = STEP_SIZE_TEST)
duration = datetime.now() - start
print("Training completed in time: ", duration)

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
import matplotlib.pyplot as plt

# Load the dataset
url = '/content/drive/MyDrive/Parkinsson disease voice data set.csv'  # Replace with the actual URL or file path
df = pd.read_csv(url)

# Extract features and labels
X = df.drop(['name', 'status'], axis=1)  # Exclude 'name' column
y = df['status']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Reshape features for CNN input (assuming one-dimensional input)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Build the neural network model with CNN layers
model2 = Sequential()
model2.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
model2.add(BatchNormalization())
model2.add(MaxPooling1D(pool_size=2))
model2.add(Conv1D(64, kernel_size=3, activation='relu'))
model2.add(BatchNormalization())
model2.add(MaxPooling1D(pool_size=2))
model2.add(Flatten())
model2.add(Dense(128, activation='relu'))
model2.add(BatchNormalization())
model2.add(Dropout(0.5))
model2.add(Dense(64, activation='relu'))
model2.add(BatchNormalization())
model2.add(Dropout(0.5))
model2.add(Dense(1, activation='sigmoid'))

# Compile the model with a lower initial learning rate
optimizer = Adam(learning_rate=0.001)
model2.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Learning rate scheduling
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

# Train the model without early stopping
history2 = model2.fit(X_train, y_train, epochs=18, batch_size=32, validation_split=0.2, callbacks=[reduce_lr])



# Handwriting model training history
plt.plot(history.history["accuracy"], label='Handwriting Validation Accuracy',  color='blue')
plt.plot(history.history["loss"], label='Handwriting Validation Loss', color='orange')

plt.plot(history2.history['val_accuracy'], label='Voice Validation Accuracy', color='red')
plt.plot(history2.history['val_loss'], label='Voice Validation Loss', color='green')

plt.xlabel('Epochs')
plt.ylabel('Accuracy / Loss')
plt.legend()
plt.title('Comparison of features')
plt.show()