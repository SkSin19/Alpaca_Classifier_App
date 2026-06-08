from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
from keras.utils import img_to_array
import base64
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model("SimpleCNN.h5")

class PredictRequest(BaseModel):
    image: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(request: PredictRequest):
    try:
        image_data = base64.b64decode(request.image)
        img = Image.open(io.BytesIO(image_data)).convert("RGB").resize((160, 160))
        img_array = img_to_array(img) / 255.0
        prediction = model.predict(img_array.reshape(1, 160, 160, 3))
        score = float(prediction[0][0])
        label = "Alpaca" if score > 0.5 else "Not Alpaca"
        print(f"Score: {score}, Label: {label}")  # add this
        return {"prediction": label, "confidence": score, "success": True}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}