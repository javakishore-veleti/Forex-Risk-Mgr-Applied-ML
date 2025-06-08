from flask import Flask
from routes.data_gen_api import data_generator_bp
from routes.risk_analysis import risk_analysis_bp
from routes.trade_positions import trade_positions_bp
from routes.volatility import volatility_bp

app = Flask(__name__)

# Register API Blueprints (Modular Routes)
app.register_blueprint(data_generator_bp, url_prefix="/data")
app.register_blueprint(risk_analysis_bp, url_prefix="/risk-analysis")
app.register_blueprint(trade_positions_bp, url_prefix="/trade-positions")
app.register_blueprint(volatility_bp, url_prefix="/volatility")

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "API is running"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
