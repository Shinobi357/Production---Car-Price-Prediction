import os
import sys
import logging
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

from preprocess import prepare_data


logging.basicConfig(
    filename="outputs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def evaluate_model(model, X_train, X_test, y_train, y_test):
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    return {
        "train_r2": r2_score(y_train, train_preds),
        "validation_r2": r2_score(y_test, test_preds),
        "mae": mean_absolute_error(y_test, test_preds),
        "rmse": mean_squared_error(y_test, test_preds) ** 0.5
    }


def train_models(data_path: str):
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    X_train, X_test, y_train, y_test, preprocessor = prepare_data(data_path)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            random_state=42
        )
    }

    results = []
    best_model = None
    best_rmse = float("inf")

    for name, estimator in models.items():
        logging.info(f"Training model: {name}")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator)
            ]
        )

        pipeline.fit(X_train, y_train)

        metrics = evaluate_model(
            pipeline,
            X_train,
            X_test,
            y_train,
            y_test
        )

        cv_scores = cross_val_score(
            pipeline,
            X_train,
            y_train,
            cv=5,
            scoring="r2"
        )

        metrics["model"] = name
        metrics["cv_r2_mean"] = cv_scores.mean()
        metrics["cv_r2_std"] = cv_scores.std()

        results.append(metrics)

        logging.info(f"{name} metrics: {metrics}")

        if metrics["rmse"] < best_rmse:
            best_rmse = metrics["rmse"]
            best_model = pipeline

    results_df = pd.DataFrame(results)
    results_df.to_csv("outputs/model_results.csv", index=False)

    joblib.dump(best_model, "models/car_price_model.pkl")

    logging.info("Best model saved to models/car_price_model.pkl")
    logging.info("Training complete")

    print(results_df)
    print("\nBest model saved to models/car_price_model.pkl")


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/car_price_prediction.csv"
    train_models(data_path)
