import json
import pandas as pd
import numpy as np

from flask import Blueprint, jsonify
from data_generator.data_generator import generate_forex_data

# Create a blueprint for synthetic data API
data_gen_bp = Blueprint("data_gen_api", __name__)

# Load currency pairs from config file
CONFIG_FILE = "data-gen-config.json"

def load_currency_pairs():
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    return config["currency_pairs"], config["default_days"]

def generate_forex_data():
    currency_pairs, default_days = load_currency_pairs()
    synthetic_data = []

    for pair in currency_pairs:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=default_days, freq="D")
        prices = np.random.normal(loc=1.2, scale=0.05, size=default_days)  # Simulated price movements
        volumes = np.random.randint(1000, 5000, size=default_days)  # Simulated trade volumes

        df = pd.DataFrame({"date": dates, "currency_pair": pair, "price": prices, "volume": volumes})
        synthetic_data.append(df)

    return pd.concat(synthetic_data, ignore_index=True)

@data_gen_bp.route("/generate-data", methods=["GET"])
def generate_data():
    """
    API endpoint to generate synthetic FOREX trading data.
    
    Returns:
        JSON response containing generated data.
    """
    try:
        data = generate_forex_data()
        return jsonify({"status": "success", "generated_data": data.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
