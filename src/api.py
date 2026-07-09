from flask import Flask, request, jsonify
import logging
from src.predict import make_prediction

app = Flask(__name__)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

REQUIRED_FIELDS = [
    "Year",
    "Brand",
    "Model",
    "Mileage",
    "Fuel_Type",
    "Transmission",
    "Condition"
]


@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Car Price Prediction API</h1>
    <p>Use POST /predict to submit car features and receive a predicted price.</p>
    <p>Use GET /health to check API status.</p>
    """


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            logging.warning("Prediction request failed: no JSON body provided")
            return jsonify({"error": "No JSON data provided"}), 400

        missing_fields = [field for field in REQUIRED_FIELDS if field not in data]

        if missing_fields:
            logging.warning(f"Prediction request failed: missing fields {missing_fields}")
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        prediction = make_prediction(data)

        logging.info(f"Prediction successful: {prediction}")

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        }), 200

    except Exception as error:
        logging.error(f"Prediction error: {str(error)}")
        return jsonify({
            "error": "Prediction failed",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
