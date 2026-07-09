from flask import Flask, request, jsonify
import logging
from predict import predict_price

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
    "Fuel Type",
    "Transmission",
    "Condition"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Car Price Prediction API",
        "endpoints": ["/health", "/predict"]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        logging.warning("No JSON data provided")
        return jsonify({"error": "No JSON data provided"}), 400

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        logging.warning(f"Missing fields: {missing}")
        return jsonify({"error": "Missing required fields", "missing_fields": missing}), 400

    try:
        prediction = predict_price(data)
        logging.info(f"Prediction successful: {prediction}")
        return jsonify({"predicted_price": round(float(prediction), 2)}), 200
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Car Price Prediction</h1>

    <form action="/predict_form" method="post">
        <label>Brand:</label><br>
        <input name="Brand" value="Toyota"><br><br>

        <label>Year:</label><br>
        <input name="Year" value="2018"><br><br>

        <label>Engine Size:</label><br>
        <input name="Engine Size" value="2.5"><br><br>

        <label>Fuel Type:</label><br>
        <input name="Fuel Type" value="Petrol"><br><br>

        <label>Transmission:</label><br>
        <input name="Transmission" value="Automatic"><br><br>

        <label>Mileage:</label><br>
        <input name="Mileage" value="55000"><br><br>

        <label>Condition:</label><br>
        <input name="Condition" value="Used"><br><br>

        <label>Model:</label><br>
        <input name="Model" value="Camry"><br><br>

        <button type="submit">Predict Price</button>
    </form>
    """

@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        data = {
            "Brand": request.form["Brand"],
            "Year": int(request.form["Year"]),
            "Engine Size": float(request.form["Engine Size"]),
            "Fuel Type": request.form["Fuel Type"],
            "Transmission": request.form["Transmission"],
            "Mileage": int(request.form["Mileage"]),
            "Condition": request.form["Condition"],
            "Model": request.form["Model"]
        }

        prediction = predict_price(data)

        return f"""
        <h1>Prediction Result</h1>
        <p>Predicted Price: ${prediction:,.2f}</p>
        <a href="/">Make another prediction</a>
        """

    except Exception as e:
        return f"""
        <h1>Error</h1>
        <p>{str(e)}</p>
        <a href="/">Try again</a>
        """