import json
import os
 
import numpy as np
from PIL import Image
import tensorflow as tf
import valohai as vh

model = tf.keras.models.load_model(vh.inputs('model').path())

def load_image(image_path):
    image_name = os.path.basename(image_path)
    image = Image.open(image_path)
    image.load()
 
    image = image.resize((28, 28)).convert('L')
    image_data = np.array(image).reshape(1, 28, 28)
    image_data = image_data / 255.0
 
    return (image_name, image_data)

def run_inference(image):
    image_name, image_data = image
    prediction = np.argmax(model.predict(image_data))
 
    with vh.logger() as logger:
        logger.log('image', image_name)
        logger.log('inferred_digit', prediction)
 
    return {
        'image': image_name,
        'inferred_digit': str(prediction),
    }

results = []
for path in vh.inputs('images').paths():
    results.append(run_inference(load_image(path)))
 
with open(vh.outputs().path('results.json'), 'w') as f:
    json.dump(results, f)
