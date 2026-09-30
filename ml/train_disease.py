import tensorflow as tf
from tensorflow.keras import layers, models
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = BASE_DIR / "plantvillage_data" / "images"
MODEL_PATH = BASE_DIR / "model" / "disease_model.keras"
CLASS_PATH = BASE_DIR / "model" / "class_names.txt"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names

print("================================")
print("Classes:", len(class_names))
print("================================")

for name in class_names:
    print(name)

os.makedirs(MODEL_PATH.parent, exist_ok=True)

with open(CLASS_PATH, "w") as f:
    for name in class_names:
        f.write(name + "\n")

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    layers.Rescaling(1.0 / 255),

    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),

    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(256, activation="relu"),
    layers.Dropout(0.4),

    layers.Dense(len(class_names), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Starting training...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=15
)

model.save(MODEL_PATH)

print()
print("======================================")
print("38-CLASS DISEASE MODEL TRAINING DONE")
print("======================================")
print("Model:", MODEL_PATH)
print("Classes:", CLASS_PATH)
print("======================================")