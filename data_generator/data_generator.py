import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from util.MongoDBConnFacade import MongoDBConnFacade

# Initialize MongoDB Connection
mongo = MongoDBConnFacade.getInstance()

# Predefined currency market baselines for realism
currency_trend_baselines = {
    "EUR/USD": {"mean": 1.20, "volatility": max(0.008, 0.004), "drift_factor": 0.0004},
    "USD/JPY": {"mean": 110.0, "volatility": max(0.8, 0.4), "drift_factor": 0.04},
    "GBP/USD": {"mean": 1.35, "volatility": max(0.015, 0.007), "drift_factor": 0.0009},
    "AUD/USD": {"mean": 0.75, "volatility": max(0.007, 0.003), "drift_factor": 0.0002},
    "USD/CAD": {"mean": 1.25, "volatility": max(0.012, 0.006), "drift_factor": 0.0003}
}

def generate_customers():
    """Generate 1000 customers only if the collection is empty."""
    if mongo.is_collection_empty("Customers"):
        customers = [{"customer_id": i + 1, "name": f"Customer_{i + 1}", "country": "USA",
                      "balance": random.uniform(1000, 100000)} for i in range(1000)]
        mongo.save("Customers", customers)

def generate_traders():
    """Generate 15 traders only if the collection is empty."""
    if mongo.is_collection_empty("Traders"):
        traders = [{"trader_id": i + 1, "name": f"Trader_{i + 1}", "experience_years": random.randint(1, 10)} for i in range(15)]
        mongo.save("Traders", traders)

def generate_trading_books():
    """Generate 10 trading books only if the collection is empty."""
    if mongo.is_collection_empty("TradingBooks"):
        books = [{"book_id": i + 1, "name": f"Book_{i + 1}",
                  "strategy": random.choice(["Momentum", "Mean Reversion", "Arbitrage"])} for i in range(10)]
        mongo.save("TradingBooks", books)

def get_random_trading_date():
    """Generate a random trading date within the last year."""
    today = datetime.today()
    random_days = random.randint(0, 365)
    return (today - timedelta(days=random_days)).strftime("%Y-%m-%d")

def simulate_price_movement(initial_price, days=30, drift_factor=0.001, volatility_factor=0.01):
    """Simulate realistic price movements using market drift and volatility."""
    prices = [initial_price]
    for _ in range(days):
        trend_drift = drift_factor * prices[-1]  # Small consistent trend shift
        random_volatility = np.random.normal(0, max(0.001, prices[-1] * volatility_factor))  # Ensure non-negative volatility
        prices.append(prices[-1] + trend_drift + random_volatility)
    return prices

def moving_average(data, window_size=5):
    """Apply moving average smoothing to reduce extreme variations."""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def generate_trade_data():
    """Generate trade events using realistic price fluctuations, volatility, and trend-based adjustments."""
    customers, traders, books = list(mongo.get_all("Customers")), list(mongo.get_all("Traders")), list(mongo.get_all("TradingBooks"))

    if not customers or not traders or not books:
        print("⚠️ Missing entities! Cannot generate trade events.")
        return None

    trade_events = []
    currency_pairs = list(currency_trend_baselines.keys())

    for _ in range(100000):  # Generate trade events
        customer, trader, book = random.choice(customers), random.choice(traders), random.choice(books)
        chosen_pair = random.choice(currency_pairs)
        baseline = currency_trend_baselines[chosen_pair]

        # Generate price & quantity using realistic statistical modeling and trend-based adjustment
        initial_price = baseline["mean"]
        simulated_prices = simulate_price_movement(initial_price, days=30, drift_factor=baseline["drift_factor"], volatility_factor=baseline["volatility"])
        smoothed_prices = moving_average(simulated_prices, window_size=5)  # Try window_size=3 or 7 for further refinements

        from_currency_qty = round(np.random.normal(5000, max(400, 200)), 2)  # Prevent negative scale error
        to_currency_price = round(random.choice(smoothed_prices), 4)  # Use smooth price movements
        to_currency_qty = round(from_currency_qty * to_currency_price, 2)

        trade_events.append({
            "customer_id": customer["customer_id"],
            "trading_dt": get_random_trading_date(),
            "from_currency": chosen_pair.split("/")[0],
            "to_currency": chosen_pair.split("/")[1],
            "from_currency_qty": max(10, from_currency_qty),  # Avoid negative values
            "to_currency_qty": to_currency_qty,
            "from_currency_price": 1.0,
            "to_currency_price": to_currency_price,
            "trader_id": trader["trader_id"],
            "trading_book_id": book["book_id"]
        })

    if trade_events:
        mongo.save("Trade_Events", trade_events)
        print("✅ Trade events successfully stored in MongoDB!")

    return trade_events

def generate_forex_data():
    """Ensure all required data is created before generating trade events and return confirmation."""
    generate_customers(), generate_traders(), generate_trading_books()
    trade_events = generate_trade_data()

    return {
        "status": "success",
        "message": "Data generation complete.",
        "customers_created": mongo.db["Customers"].count_documents({}),
        "traders_created": mongo.db["Traders"].count_documents({}),
        "trading_books_created": mongo.db["TradingBooks"].count_documents({}),
        "trade_events_generated": len(trade_events) if trade_events else 0
    }
