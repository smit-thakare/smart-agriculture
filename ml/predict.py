import tensorflow as tf
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "model" / "disease_model.keras"
CLASS_PATH = BASE_DIR / "model" / "class_names.txt"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as file:
    class_names = [line.strip() for line in file.readlines()]


def predict_disease(image_path):

    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    image = tf.keras.utils.img_to_array(image)

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    index = np.argmax(prediction[0])

    confidence = float(prediction[0][index] * 100)

    disease = class_names[index]

    if confidence < 50:
        disease = "Low Confidence - Please Upload a Clear Supported Leaf Image"

    return disease, confidence