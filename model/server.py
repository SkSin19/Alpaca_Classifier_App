from fastapi import FastAPI
import tensorflow as tf
from keras.utils import load_img, img_to_array

app = FastAPI()

model = tf.keras.models.load_model("SimpleCNN.h5")

@app.post("/predict")
def predict(image):
    img = load_img(image, target_size=(160,160))
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    prediction = model.predict(img_array.reshape(1,160,160,3))
    return prediction

