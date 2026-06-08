import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers, models
from keras import optimizers
import keras.layers as tfl
import matplotlib.pyplot as plt
import os
from keras.utils import image_dataset_from_directory

directory = os.path.abspath("data")

batch_size = 32
img_size = (160,160)

train_dataset = image_dataset_from_directory(directory,
                     shuffle=True,
                     batch_size=batch_size,
                     image_size=img_size,
                     validation_split=0.2,
                     subset="training",
                     seed = 42)

validation_dataset = image_dataset_from_directory(directory,
                    shuffle=True,
                    batch_size=batch_size,
                    image_size=img_size,
                    validation_split=0.2,
                    subset="validation",
                    seed = 42)

class_names = train_dataset.class_names

model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(160,160,3)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
])
# Complete the model
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(len(class_names), activation='softmax'))

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(train_dataset, validation_data=validation_dataset, epochs=10)

# Evaluate
loss, accuracy = model.evaluate(validation_dataset)
print(f"Validation accuracy: {accuracy:.2f}")

# Save model
model.save('SimpleCNN.h5')
