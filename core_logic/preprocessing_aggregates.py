import logging
import datetime
import time
from util import MongoDBConnFacade


class PreProcessingAggregates:

    def __init__(self):
        pass

    @staticmethod
    def preprocess_trade_data_aggregates():
        """Execute MongoDB aggregation pipeline and update only modified records."""
        logging.info("🚀 Starting trade event aggregation process...")

        mongo = MongoDBConnFacade.MongoDBConnFacade.getInstance()
        start_time = time.time()  # ✅ Capture start time

        # Ensure a unique index on trade_event_date for proper upserts
        mongo.db["Trade_Events_Aggregates"].create_index("trade_event_date", unique=True)

        # Run aggregation and store unique trade event dates
        pipeline = [
            {"$group": {
                "_id": "$trading_dt",
                "trade_event_date": {"$first": "$trading_dt"},
                "daily_high": {"$max": "$to_currency_price"},
                "daily_low": {"$min": "$to_currency_price"}
            }},
            {"$addFields": {
                "price_range": {"$subtract": ["$daily_high", "$daily_low"]},
                "aggregate_last_run_date": datetime.datetime.utcnow(),
                "aggregate_last_run_time_taken_millis": round((time.time() - start_time) * 1000)
            }},
            {"$merge": {
                "into": "Trade_Events_Aggregates",
                "on": "trade_event_date",
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }}
        ]

        # Execute aggregation and fetch updated trade event dates
        result = list(mongo.db["Trade_Events"].aggregate(pipeline))
        updated_dates = [r["trade_event_date"] for r in result]

        execution_time = round((time.time() - start_time) * 1000)  # ✅ Calculate execution duration

        # **Update only relevant records**
        if updated_dates:
            update_result = mongo.db["Trade_Events_Aggregates"].update_many(
                {"trade_event_date": {"$in": updated_dates}},  # ✅ Restrict updates ONLY to modified dates
                {"$set": {"aggregate_last_run_time_taken_millis": execution_time}}
            )
            logging.info(f"✅ Updated {update_result.modified_count} records with execution time.")

        logging.info(f"✅ Aggregation process completed in {execution_time} ms!")
        return {
            "message": "✅ Trade event aggregates created in `Trade_Events_Aggregates`.",
            "aggregate_last_run_date": datetime.datetime.utcnow(),
            "aggregate_last_run_time_taken_millis": execution_time,
            "updated_dates": updated_dates
        }
