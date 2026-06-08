#this model is overfitted so dont use this - i just wrote this once more in a bit different way for fun and practice


import tensorflow as tf
from keras import layers, models
from keras import optimizers
import pandas as pd
import numpy as np
import keras.layers as tfl
from keras.utils import image_dataset_from_directory


train_dataset = tf.keras.utils.image_dataset_from_directory(
    "data",
    shuffle=True,
    batch_size=32,
    image_size=(160,160)
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    "data",
    batch_size=32,
    image_size=(160,160),
    shuffle=True
)


model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(160,160,3)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss = 'sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(train_dataset, validation_data=validation_dataset, epochs=10)

accuracy = model.evaluate(validation_dataset)[1]
print(f"Validation accuracy: {accuracy:.2f}")

if(accuracy > 0.95):
    model.save("SimpleCNN_practice.h5")
else:
    print("Better luck next time kiddo")