from flask import Blueprint, jsonify
from data_generator.data_generator import generate_forex_data

# Create a blueprint for synthetic data API
risk_analysis_bp = Blueprint("risk_analysis_api", __name__)
