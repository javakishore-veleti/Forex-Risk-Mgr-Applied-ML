from flask import Blueprint, jsonify
from data_generator.data_generator import generate_forex_data

# Create a blueprint for synthetic data API
trade_positions_bp = Blueprint("trade_positions_api", __name__)
