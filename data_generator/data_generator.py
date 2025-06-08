import pandas as pd
import numpy as np
from util.MongoDBConnFacade import MongoDBConnFacade
import random
from datetime import datetime, timedelta
import random
mongo = MongoDBConnFacade.getInstance()


def generate_customers():
    """Generate 1000 customers only if the collection is empty."""
    if mongo.is_collection_empty("Customers"):
        customers = [{"customer_id": i + 1, "name": f"Customer_{i + 1}", "country": "USA",
                      "balance": random.uniform(1000, 100000)} for i in range(1000)]
        mongo.save("Customers", customers)


def generate_traders():
    """Generate 15 traders only if the collection is empty."""
    if mongo.is_collection_empty("Traders"):
        traders = [{"trader_id": i + 1, "name": f"Trader_{i + 1}", "experience_years": random.randint(1, 10)} for i in
                   range(15)]
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
    one_year_ago = today - timedelta(days=365)

    # Generate a random date between one_year_ago and today
    random_days = random.randint(0, 365)
    random_date = one_year_ago + timedelta(days=random_days)

    return random_date.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD

def generate_trade_data():
    """Generate trade events using existing customers, traders, and trading books."""
    customers = list(mongo.get_all("Customers"))
    traders = list(mongo.get_all("Traders"))
    books = list(mongo.get_all("TradingBooks"))

    print(f"Retrieved {len(customers)} customers, {len(traders)} traders, {len(books)} trading books.")

    if not customers or not traders or not books:
        print("⚠️ Missing entities! Cannot generate trade events.")
        return None

    trade_events = []
    currency_pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/CAD"]

    for _ in range(100000):  # Generate 5000 trade events
        customer = random.choice(customers)
        trader = random.choice(traders)
        book = random.choice(books)
        from_currency, to_currency = random.choice(currency_pairs).split("/")
        from_currency_qty = round(random.uniform(100, 10000), 2)
        to_currency_price = round(random.uniform(1.1, 1.5), 4)
        to_currency_qty = round(from_currency_qty * to_currency_price, 2)

        trade_events.append({
            "customer_id": customer["customer_id"],
            "trading_dt": get_random_trading_date(),
            "from_currency": from_currency,
            "to_currency": to_currency,
            "from_currency_qty": from_currency_qty,
            "to_currency_qty": to_currency_qty,
            "from_currency_price": 1.0,
            "to_currency_price": to_currency_price,
            "trader_id": trader["trader_id"],
            "trading_book_id": book["book_id"]
        })

    if not trade_events:
        print("⚠️ No trade events generated!")
        return None

    mongo.save("Trade_Events", trade_events)
    print("✅ Trade events successfully stored in MongoDB!")
    return trade_events

def generate_forex_data():
    """Ensure all required data is created before generating trade events and return confirmation."""

    # Create Customers, Traders, and Trading Books (only if empty)
    generate_customers()
    generate_traders()
    generate_trading_books()

    # Generate trade events based on the created customers, traders, and books
    trade_events = generate_trade_data()

    return {
        "status": "success",
        "message": "Data generation complete.",
        "customers_created": mongo.db["Customers"].count_documents({}),
        "traders_created": mongo.db["Traders"].count_documents({}),
        "trading_books_created": mongo.db["TradingBooks"].count_documents({}),
        "trade_events_generated": len(trade_events) if trade_events else 0
    }




