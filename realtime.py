from fastapi import FastAPI, File, UploadFile
from starlette.requests import Request
import tensorflow as tf
import numpy
from PIL import Image
from io import BytesIO
import os
 
app = FastAPI()
 
model_path = 'model.h5'
loaded_model = None

# Call this method when our endpoint is called 
# by sending a HTTP POST message to /predict-digit
@app.post("/predict-digit")
async def predict(image: UploadFile = File(...)):
    img = Image.open(BytesIO(await image.read()))
 
    # Resize image and convert to grayscale
    img = img.resize((28, 28)).convert('L')
    img_array = numpy.array(img)
 
    image_data = numpy.reshape(img_array, (1, 28, 28))
 
    # We don't want to laod more for every request, just once
    # So we check if the model is already loaded
    global loaded_model
    if not loaded_model:
        loaded_model = tf.keras.models.load_model(model_path)
 
    # Predict with the model
    prediction = loaded_model.predict_classes(image_data)
 
    return f'Predicted_Digit: {prediction[0]}'

# Middleware to route requests
# A valohai endpoint isn't on /predict but instead a auto-generated URL like:
# https://valohai.cloud/organisation-name/projecct-name/deployment-name/deployment-version/predict-digit 
# So we need to make sure we take into account "/organisation-name/projecct-name/deployment-name/deployment-version/"
# when routing our requests to /predict-digit
@app.middleware("http")
async def process_valohai_prefix(request: Request, call_next):
    path = request.scope["path"]
    # Check if this endpoint has requests headers or an environment variable that tells us it's hosted on Valohai
    for prefix in (
        request.headers.get("X-VH-Prefix"),
        os.environ.get("VH_DEFAULT_PREFIX"),
    ):
        if not prefix:  # Could have no header or no envvar, so skip
            continue
        if path.startswith(prefix):  # If the path starts with this prefix,
            # ... tell FastAPI (0.56.0+) that that is the prefix we're mounted under...
            request.scope["root_path"] = prefix
            # ... then strip the prefix out as far as FastAPI is concerned.
            request.scope["path"] = "/" + path[len(prefix) :].lstrip("/")
            break
    return await call_next(request)
