import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "dataset" / "yield_data.csv"
MODEL_PATH = BASE_DIR / "model" / "yield_model.pkl"


print("Loading dataset...")
print("Dataset path:", DATA_PATH)

if not DATA_PATH.exists():
    print("ERROR: yield_data.csv was not found!")
    print("Expected location:")
    print(DATA_PATH)
    exit()


df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print("Total records:", len(df))
print("Total crops:", df["Crop"].nunique())


X = df[
    [
        "Crop",
        "Area",
        "Rainfall",
        "Temperature",
        "Humidity",
        "Soil_pH",
        "Fertilizer"
    ]
]

y = df["Yield"]


categorical_features = ["Crop"]

numeric_features = [
    "Area",
    "Rainfall",
    "Temperature",
    "Humidity",
    "Soil_pH",
    "Fertilizer"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "crop",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            StandardScaler(),
            numeric_features
        )
    ]
)


model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training model...")

model.fit(X_train, y_train)


predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)


print()
print("======================================")
print("     YIELD MODEL TRAINING COMPLETE")
print("======================================")
print("Total records :", len(df))
print("Total crops   :", df["Crop"].nunique())
print()
print("Crops included:")
for crop in sorted(df["Crop"].unique()):
    print("-", crop)

print()
print("MAE           :", mae)
print("R2 Score      :", r2)
print()
print("Model saved   :", MODEL_PATH)
print("======================================")