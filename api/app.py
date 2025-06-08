from flask import Flask
from api.routes.data_gen_api import data_gen_bp
from api.routes.preprocess_trade_data import pre_process_trade_data_bp
from api.routes.risk_analysis import risk_analysis_bp
from api.routes.trade_positions import trade_positions_bp
from api.routes.volatility import volatility_bp

app = Flask(__name__)

# Register API Blueprints (Modular Routes)
app.register_blueprint(data_gen_bp, url_prefix="/data")
app.register_blueprint(risk_analysis_bp, url_prefix="/risk-analysis")
app.register_blueprint(trade_positions_bp, url_prefix="/trade-positions")
app.register_blueprint(volatility_bp, url_prefix="/volatility")
app.register_blueprint(pre_process_trade_data_bp, url_prefix="/preprocess")

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "API is running"}


@app.route("/", methods=["GET"])
def home():
    return {"message": "Welcome to Forex Risk Manager API"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
