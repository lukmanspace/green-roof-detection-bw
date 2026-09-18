from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "green_roof_rf.joblib"
)

FEATURES = [
    "slope_deg",
    "area_m2",
    "height_m",
    "height_relief_m",
    "G_avg_Winter",
    "B_avg_Winter",
    "NDVI_avg_Winter",
    "NDVI_std_Winter",
    "G_avg_Summer",
    "B_avg_Summer",
    "NDVI_avg_Summer",
    "NDVI_std_Summer",
    "roofType",
    "function",
]


def load_model():
    return joblib.load(MODEL_PATH)


def predict(df):
    model = load_model()

    X = df[FEATURES].copy()

    probabilities = model.predict_proba(X)[:, 1]

    result = df.copy()
    result["green_roof_probability"] = probabilities

    return result


if __name__ == "__main__":

    df = pd.read_csv("examples/example_input.csv")

    result = predict(df)

    print(result[
        ["green_roof_probability"]
    ])