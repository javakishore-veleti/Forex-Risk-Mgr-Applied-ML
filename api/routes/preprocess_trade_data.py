from flask import Blueprint, jsonify

from core_logic.preprocessing import PreProcessing

# Create a blueprint for synthetic data API
pre_process_trade_data_bp = Blueprint("preprocess_trade_data_api", __name__)


@pre_process_trade_data_bp.route("/preprocess-trade-data", methods=["GET"])
def preprocess_trade_data():
    """
    API endpoint to generate synthetic FOREX trading data.

    Returns:
        JSON response containing generated data.
    """
    try:
        pre_processor = PreProcessing()
        df = pre_processor.preprocess_trade_data()
        if df is None:
            return jsonify({"message": "✅ All trade events were already preprocessed!"})
        return jsonify({"message": "✅ Trade event preprocessing completed successfully!"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})
