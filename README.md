# Production---Car-Price-Prediction
Car Price Prediction

## How to Run

1. Clone the repository
2. Install requirements
3. Train the model
4. Start the API
5. Send a prediction request

pip install -r requirements.txt
python src/train.py
python src/api.py
pytest tests/test_api.py
docker build -t car-price-api .
docker run -p 5000:5000 car-price-api
