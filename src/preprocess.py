import os
import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib


logging.basicConfig(
    filename="outputs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_data(file_path: str) -> pd.DataFrame:
    logging.info(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    logging.info(f"Data loaded successfully with shape {df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data")

    df = df.copy()

    if "Car ID" in df.columns:
        df = df.drop(columns=["Car ID"])

    df = df.drop_duplicates()

    # Remove extreme price and mileage outliers using IQR
    for col in ["Price", "Mileage"]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    logging.info(f"Data cleaned. New shape: {df.shape}")
    return df


def build_preprocessor():
    numeric_features = ["Year", "Engine Size", "Mileage"]
    categorical_features = ["Brand", "Fuel Type", "Transmission", "Condition", "Model"]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    return preprocessor


def prepare_data(file_path: str):
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    df = load_data(file_path)
    df = clean_data(df)

    X = df.drop(columns=["Price"])
    y = df["Price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    preprocessor = build_preprocessor()

    joblib.dump(preprocessor, "models/preprocessor.pkl")

    logging.info("Preprocessor saved to models/preprocessor.pkl")

    return X_train, X_test, y_train, y_test, preprocessor
