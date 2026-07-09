# 🚗 Production Car Price Prediction API

## Project Overview

This project implements a production-ready machine learning application for predicting used car prices. The application includes a complete machine learning pipeline consisting of data preprocessing, model training, prediction through a REST API, automated testing, logging, and Docker containerization.

The model is trained using Scikit-learn and exposed through a Flask API, allowing users to submit vehicle information and receive an estimated market price.

---

## Features

- Data preprocessing pipeline
- Automated model training
- Machine learning model serialization with Joblib
- REST API built with Flask
- Health check endpoint
- Prediction endpoint
- Automated API testing using PyTest
- Application logging
- Docker container support

---

## Project Structure

```text
Production---Car-Price-Prediction
│
├── data/
│   └── car_price_prediction.csv
│
├── models/
│   └── car_price_model.pkl
│
├── notebooks/
│   └── api_demo.ipynb
│
├── outputs/
│   └── pipeline.log
│
├── src/
│   ├── api.py
│   ├── logger.py
│   ├── predict.py
│   ├── preprocess.py
│   └── train.py
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Shinobi357/Production---Car-Price-Prediction.git

cd Production---Car-Price-Prediction
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

# Train the Model

Run the training pipeline to preprocess the data, train the models, evaluate performance, and save the best model.

```bash
python src/train.py
```

The trained model will be saved to:

```text
models/car_price_model.pkl
```

---

# Run the API

Start the Flask application

```bash
python src/api.py
```

The API will be available at

```
http://127.0.0.1:5000
```

---

# API Endpoints

## Home

```
GET /
```

Returns API information.

---

## Health Check

```
GET /health
```

Example Response

```json
{
    "status":"running"
}
```

---

## Predict Vehicle Price

```
POST /predict
```

Example Request

```json
{
    "Brand":"Toyota",
    "Year":2018,
    "Engine Size":2.5,
    "Fuel Type":"Petrol",
    "Transmission":"Automatic",
    "Mileage":55000,
    "Condition":"Used",
    "Model":"Camry"
}
```

Example Response

```json
{
    "predicted_price":50945.34
}
```

---

# Run Automated Tests

Execute the API test suite using PyTest.

```bash
pytest tests/test_api.py
```

Example Output

```text
==================== 4 passed ====================
```

---

## Model Performance

The application evaluates multiple machine learning models and automatically selects the best-performing model based on validation performance.

### Models Evaluated

| Model | Training R² | Validation R² |
|--------|------------:|--------------:|
| Linear Regression | 0.02 | -0.02 |
| Random Forest | 0.52 | -0.03 |

### Evaluation Metrics

- **R² Score** – Measures how well the model explains the variance in vehicle prices.
- **Mean Absolute Error (MAE)** – Average prediction error in dollars.
- **Root Mean Squared Error (RMSE)** – Penalizes larger prediction errors.

The best-performing model is automatically serialized and saved as:

```text
models/car_price_model.pkl


```

# Docker

Build the Docker image

```bash
docker build -t car-price-api .
```

Run the Docker container

```bash
docker run -p 5000:5000 car-price-api
```

---

# Machine Learning Workflow

1. Load the dataset
2. Clean and preprocess the data
3. Split into training and testing datasets
4. Train multiple regression models
5. Evaluate each model using:
   - R² Score
   - Mean Absolute Error (MAE)
   - Root Mean Squared Error (RMSE)
6. Select the best-performing model
7. Save the model with Joblib
8. Serve predictions through the Flask API

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Flask
- Joblib
- Docker
- PyTest
- Git
- GitHub
- JupyterLab

---

# Future Improvements

- Hyperparameter optimization using GridSearchCV
- Continuous Integration / Continuous Deployment (CI/CD)
- Cloud deployment using AWS SageMaker
- Model monitoring and drift detection
- Interactive web interface
- Authentication and API security

---

## Project Purpose

This project was completed as part of the Springboard Machine Learning Engineering Career Track. The objective was to demonstrate the complete machine learning lifecycle, from data preprocessing and model training to deployment of a production-ready REST API.

---

# Author

**Christopher Lawrence**

GitHub:

https://github.com/Shinobi357
