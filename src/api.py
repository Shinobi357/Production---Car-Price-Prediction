import logging
import os

from flask import Flask, jsonify, render_template, request

from predict import predict_price


app = Flask(__name__)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

REQUIRED_FIELDS = [
    "Year",
    "Brand",
    "Model",
    "Mileage",
    "Fuel Type",
    "Transmission",
    "Condition",
    "Engine Size",
]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "running",
            "message": "Car Price Prediction API is healthy",
        }
    ), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data:
        logging.warning("No JSON data provided")
        return jsonify({"error": "No JSON data provided"}), 400

    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in data or str(data[field]).strip() == ""
    ]

    if missing:
        logging.warning("Missing fields: %s", missing)
        return jsonify(
            {
                "error": "Missing required fields",
                "missing_fields": missing,
            }
        ), 400

    try:
        cleaned_data = {
            "Brand": str(data["Brand"]).strip(),
            "Model": str(data["Model"]).strip(),
            "Year": int(data["Year"]),
            "Engine Size": float(data["Engine Size"]),
            "Fuel Type": str(data["Fuel Type"]).strip(),
            "Transmission": str(data["Transmission"]).strip(),
            "Mileage": float(data["Mileage"]),
            "Condition": str(data["Condition"]).strip(),
        }

        prediction = predict_price(cleaned_data)

        logging.info(
            "Prediction successful. Input=%s Prediction=%s",
            cleaned_data,
            prediction,
        )

        return jsonify(
            {
                "predicted_price": round(float(prediction), 2),
            }
        ), 200

    except ValueError as exc:
        logging.exception("Invalid numeric input")
        return jsonify(
            {
                "error": "Invalid input",
                "details": str(exc),
            }
        ), 400

    except Exception as exc:
        logging.exception("Prediction failed")
        return jsonify(
            {
                "error": "Prediction failed",
                "details": str(exc),
            }
        ), 500


@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        data = {
            "Brand": request.form["Brand"].strip(),
            "Model": request.form["Model"].strip(),
            "Year": int(request.form["Year"]),
            "Engine Size": float(request.form["Engine Size"]),
            "Fuel Type": request.form["Fuel Type"].strip(),
            "Transmission": request.form["Transmission"].strip(),
            "Mileage": float(request.form["Mileage"]),
            "Condition": request.form["Condition"].strip(),
        }

        prediction = predict_price(data)

        logging.info(
            "Form prediction successful. Input=%s Prediction=%s",
            data,
            prediction,
        )

        return render_template(
            "index.html",
            prediction=f"${float(prediction):,.2f}",
            submitted=data,
        )

    except ValueError as exc:
        logging.exception("Invalid form input")
        return render_template(
            "index.html",
            error="Year, engine size, and mileage must be valid numbers.",
        ), 400

    except Exception as exc:
        logging.exception("Form prediction failed")
        return render_template(
            "index.html",
            error=f"Prediction failed: {exc}",
        ), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
    )
