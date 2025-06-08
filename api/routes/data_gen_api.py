from flask import Blueprint, jsonify
from data_generator.data_generator import generate_forex_data

# Create a blueprint for synthetic data API
data_gen_bp = Blueprint("data_gen_api", __name__)

@data_gen_bp.route("/generate-data", methods=["GET"])
def generate_data():
    """
    API endpoint to generate synthetic FOREX trading data.
    
    Returns:
        JSON response containing generated data.
    """
    try:
        result = generate_forex_data()
        if result is None:
            return jsonify({"status": "error", "message": "No data generated"})
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})
