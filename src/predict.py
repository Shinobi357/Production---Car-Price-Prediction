from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "car_price_model.pkl"

model_pipeline = joblib.load(MODEL_PATH)


def predict_price(data: dict) -> float:
    input_df = pd.DataFrame([data])

    prediction = model_pipeline.predict(input_df)[0]

    return float(prediction)
