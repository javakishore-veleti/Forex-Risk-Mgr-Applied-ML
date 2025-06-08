db = db.getSiblingDB("forex_risk_mgr_db");

// Ensure Customers collection exists
if (db.Customers.countDocuments() === 0) {
    for (let i = 0; i < 1000; i++) {
        db.Customers.insertOne({
            customer_id: i + 1,
            name: "Customer_" + (i + 1),
            country: "USA",
            balance: Math.random() * 100000
        });
    }
}

// Ensure Traders collection exists
if (db.Traders.countDocuments() === 0) {
    for (let i = 0; i < 25; i++) {
        db.Traders.insertOne({
            trader_id: i + 1,
            name: "Trader_" + (i + 1),
            experience_years: Math.floor(Math.random() * 10) + 1
        });
    }
}

// Ensure TradingBooks collection exists
if (db.TradingBooks.countDocuments() === 0) {
    for (let i = 0; i < 10; i++) {
        db.TradingBooks.insertOne({
            book_id: i + 1,
            name: "Book_" + (i + 1),
            strategy: "Momentum"
        });
    }
}
