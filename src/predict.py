import joblib
import pandas as pd


MODEL_PATH = "models/car_price_model.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def predict_price(input_data: dict):
    model = load_model()

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    return round(float(prediction), 2)


if __name__ == "__main__":
    sample_car = {
        "Brand": "Toyota",
        "Year": 2018,
        "Engine Size": 2.5,
        "Fuel Type": "Petrol",
        "Transmission": "Automatic",
        "Mileage": 55000,
        "Condition": "Used",
        "Model": "Camry"
    }

    predicted_price = predict_price(sample_car)

    print({"predicted_price": predicted_price})
