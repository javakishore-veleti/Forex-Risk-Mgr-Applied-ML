from flask import Blueprint, jsonify
from core_logic.preprocessing_aggregates import PreProcessingAggregates

# Create a blueprint for trade data aggregation API
pre_process_trade_data_aggr_bp = Blueprint("preprocess_trade_data_aggr_api", __name__)

@pre_process_trade_data_aggr_bp.route("/preprocess-trade-data-aggregates", methods=["GET"])
def preprocess_trade_data_aggregate():
    """
    API endpoint to preprocess and aggregate FOREX trading data.

    Returns:
        JSON response confirming aggregation results.
    """
    try:
        pre_processor_aggr = PreProcessingAggregates()
        response = pre_processor_aggr.preprocess_trade_data_aggregates()

        return jsonify(response)  # ✅ Returns structured response message
    except Exception as e:
        print(f"❌ Error in preprocessing trade data aggregation: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})
