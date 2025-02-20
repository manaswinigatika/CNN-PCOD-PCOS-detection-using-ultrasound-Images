# -*- coding: utf-8 -*-
"""pcos.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B26BIhfu5FzO39fjr9dr0RKQUUlUnNr7
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import shutil
import glob
import zipfile

!unzip /content/PCOS.zip

from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix

# Set paths to your dataset
train_dir = '/content/train'
validation_dir = '/content/val'
test_dir = '/content/test'

# Data Augmentation with ImageDataGenerator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load training and validation data
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=True
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=False
)

# Load MobileNet model
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1, activation='sigmoid')
])

# Compile the model with class weights for imbalance handling
class_weights = {0: 1.0, 1: (train_generator.samples / validation_generator.samples) * (781 / 1143)}
model.compile(optimizer='RMSprop', loss='binary_crossentropy', metrics=['accuracy'])

# Callbacks for early stopping and saving the best model
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint('best_model.keras', save_best_only=True)
]

# Train the model with class weights
history = model.fit(
    train_generator,
    epochs=50,
    validation_data=validation_generator,
    class_weight=class_weights,
    callbacks=callbacks
)

# Evaluate the model on test data
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=False
)

predictions = model.predict(test_generator)
predicted_classes = np.where(predictions > 0.5, 1, 0)

# Generate classification report and confusion matrix
print(classification_report(test_generator.classes, predicted_classes))
print(confusion_matrix(test_generator.classes, predicted_classes))

# Plotting training history (optional)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()



ROOT_DIR = '/content/PCOS'
number_of_images = {}

for dir in os.listdir(ROOT_DIR):
   number_of_images[dir] = len(os.listdir(os.path.join(ROOT_DIR,dir)))
   print("",dir,"" ,number_of_images[dir])

!pip install tensorflow
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet import preprocess_input

def preprocessingImage1(path):
  image_data = ImageDataGenerator(zoom_range=0.2,shear_range=0.2,preprocessing_function= preprocess_input,horizontal_flip=True)
  image = image_data.flow_from_directory(directory=path,target_size=(224,224),batch_size=32,class_mode='binary')
  return image

def preprocessionfImage2(path):
  """
  Input :path
  Output : preprocessed Image
  """
  image_data  = ImageDataGenerator(preprocessing_function= preprocess_input )
  image = image_data.flow_from_directory(directory=path,target_size=(224,224),batch_size=32,class_mode='binary')

  return image

""" 70% for training 15 % for vailadation 15 % for testing"""

def datafolder(path,split):
  if not os.path.exists("./"+path):
    os.mkdir("./"+path)

    for dir in os.listdir(ROOT_DIR):
      os.makedirs("./"+path+"/"+dir)
      for img in np.random.choice(a=os.listdir(os.path.join(ROOT_DIR,dir)),
                                  size=(math.floor(split * number_of_images[dir])-5),replace=False):

          O = os.path.join(ROOT_DIR,dir,img)
          D = os.path.join("./"+path,dir)
          shutil.copy(O,D)
          os.remove(O)

  else:
     print("Folder already exist")

datafolder("train",0.7)


datafolder("val",0.15)


datafolder("test",0.15)

path ='/content/train'
train_data = preprocessingImage1(path)

path ='/content/test'
test_data = preprocessionfImage2(path)

path = '/content/val'
val_data = preprocessionfImage2(path)

"""Model Block"""

import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Flatten,Dense
from keras.models import Model,load_model
from keras.applications.mobilenet import MobileNet
import keras

base_model = MobileNet(input_shape=(224,224,3),include_top=False)

for layer in base_model.layers:
  layer.trainable = False



x= Flatten()(base_model.output)
x= Dense(units=1,activation='sigmoid')(x)

model = Model(base_model.input,x)

model.compile(optimizer='rmsprop',loss=keras.losses.binary_crossentropy,metrics=['accuracy'])

from keras.callbacks import ModelCheckpoint,EarlyStopping

# Change the filepath to end with .keras
mc = ModelCheckpoint(filepath="bestmodel.keras",monitor='val_accuracy',verbose=1,save_best_only=True)


es = EarlyStopping(monitor="val_accuracy",min_delta=0.01,patience=5,verbose=1)

cb = [mc,es]

hist = model.fit(train_data,
                           steps_per_epoch=1,
                           epochs=5,
                           validation_data=val_data,
                           validation_steps=16,
                          callbacks=cb)

# Change the file extension to '.keras' to match the ModelCheckpoint configuration.
model = load_model("/content/bestmodel.keras")

acc = model.evaluate(test_data)[1]
print(f"our model accuracy is  {acc * 100} %")

h = hist.history
h.keys()

train_data.class_indices

test_data.class_indices

val_data.class_indices

from keras.preprocessing import image
import tensorflow as tf


def predictimage(path):

      img = tf.keras.utils.load_img(path,target_size=(224,224))
      i = tf.keras.utils.img_to_array(img)/255
      input_arr= np.array([i])
      input_arr.shape

      pred =model.predict(input_arr)
      if pred == 1:
          print("Not Affected")
      else :
         print("Affected")
      #display image
      plt.imshow(input_arr[0],vmin=0, vmax=255)
      plt.title("input Image")
      plt.show()

predictimage("/content/train/infected/img_0_1257.jpg")

predictimage("/content/train/notinfected/img_0_1123.jpg")

predictimage("/content/test/infected/img_0_1272.jpg")



from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import numpy as np

# Generate predictions on the test data
test_steps = len(train_data)  # Ensure you get predictions for the whole dataset
test_data.reset()
predictions = model.predict(train_data, steps=test_steps, verbose=1)
predicted_classes = (predictions > 0.5).astype("int32").flatten()

# True classes
true_classes = train_data.classes
class_labels = list(train_data.class_indices.keys())

# Compute confusion matrix
conf_matrix = confusion_matrix(true_classes, predicted_classes)
print("Confusion Matrix:")
print(conf_matrix)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.title('Confusion Matrix')
plt.show()

# Classification report
report = classification_report(true_classes, predicted_classes, target_names=class_labels)
print("Classification Report:")
print(report)

# Accuracy score
accuracy = accuracy_score(true_classes, predicted_classes)
print(f"Test Accuracy: {accuracy * 100:.2f}%")