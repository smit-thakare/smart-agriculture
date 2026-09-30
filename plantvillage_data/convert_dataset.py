import pandas as pd
from pathlib import Path
from PIL import Image
import io

parquet_file = Path("plantvillage_data/train-00000-of-00001.parquet")
output_dir = Path("plantvillage_data/images")

print("Loading dataset...")

df = pd.read_parquet(parquet_file)

print("Total images:", len(df))
print("Total classes:", df["class_label"].nunique())

output_dir.mkdir(parents=True, exist_ok=True)

for i, row in df.iterrows():

    class_name = str(row["class_label"])
    class_dir = output_dir / class_name
    class_dir.mkdir(parents=True, exist_ok=True)

    image_data = row["image"]

    if isinstance(image_data, dict):
        image_bytes = image_data["bytes"]
    else:
        image_bytes = image_data

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image.save(class_dir / f"{i}.jpg")

    if (i + 1) % 100 == 0:
        print(f"{i + 1}/{len(df)} converted")

print("DONE")
print("Images:", len(df))
print("Classes:", df["class_label"].nunique())