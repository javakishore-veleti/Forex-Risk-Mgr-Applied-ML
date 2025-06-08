from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, QuantileTransformer, \
    PowerTransformer
from util import MongoDBConnFacade
import pandas as pd2
import pymongo


class PreProcessing:

    def __init__(self):
        pass

    @staticmethod
    def load_trade_data():
        """Load trade events from MongoDB that haven't been preprocessed."""
        mongo = MongoDBConnFacade.MongoDBConnFacade.getInstance()
        trade_events = list(mongo.db["Trade_Events"].find({"ml_pipeline_status.preprocessing": {"$ne": True}}))
        return pd2.DataFrame(trade_events) if trade_events else None

    @staticmethod
    def clean_data(df):
        """Preserve original values and store cleaned versions separately."""
        df["trading_dt_cleaned"] = pd2.to_datetime(df["trading_dt"])  # New column
        return df

    @staticmethod
    def handle_missing_values(df):
        """Generate multiple missing-value strategies without modifying original fields."""
        fields_to_process = ["from_currency_qty", "to_currency_qty", "from_currency_price", "to_currency_price"]

        for field in fields_to_process:
            # Always create `_ffill` first
            df[f"{field}_ffill"] = df[field].ffill()

            # Apply other techniques using `_ffill` as baseline
            df[f"{field}_bfill"] = df[f"{field}_ffill"].bfill()
            df[f"{field}_interpolated"] = df[f"{field}_ffill"].interpolate(method="linear")
            df[f"{field}_rolling_avg"] = df[f"{field}_ffill"].rolling(window=7, min_periods=1).mean()
            df[f"{field}_median_fill"] = df[f"{field}_ffill"].fillna(df[f"{field}_ffill"].median())
            df[f"{field}_mean_fill"] = df[f"{field}_ffill"].fillna(df[f"{field}_ffill"].mean())

        return df

    @staticmethod
    def scale_features(df):
        """Apply multiple scaling techniques to numerical fields."""
        fields_to_scale = ["from_currency_qty", "to_currency_qty", "from_currency_price", "to_currency_price"]

        # Initialize scalers
        scalers = {
            "standard_scaled": StandardScaler(),
            "minmax_scaled": MinMaxScaler(),
            "maxabs_scaled": MaxAbsScaler(),
            "robust_scaled": RobustScaler(),
            "quantile_transformed": QuantileTransformer(output_distribution="uniform"),
            "power_transformed": PowerTransformer(method="yeo-johnson")
        }

        for field in fields_to_scale:
            for scaler_name, scaler in scalers.items():
                df[f"{field}_{scaler_name}"] = scaler.fit_transform(df[[field]])

        return df

    @staticmethod
    def add_time_features(df):
        """Generate time-based trading features."""
        df["month"] = df["trading_dt_cleaned"].dt.month
        df["week"] = df["trading_dt_cleaned"].dt.isocalendar().week
        df["day_of_week"] = df["trading_dt_cleaned"].dt.dayofweek

        # Rolling price volatility (7-day window)
        df["price_volatility"] = df["to_currency_price"].rolling(window=7).std()

        return df

    @staticmethod
    def update_pipeline_status(trade_ids):
        """Mark preprocessing as completed in MongoDB using bulk updates for efficiency."""
        mongo = MongoDBConnFacade.MongoDBConnFacade.getInstance()
        bulk_updates = [
            pymongo.UpdateOne({"_id": trade_id}, {"$set": {"ml_pipeline_status.preprocessing": True}})
            for trade_id in trade_ids
        ]
        if bulk_updates:
            mongo.db["Trade_Events"].bulk_write(bulk_updates)

    @staticmethod
    def preprocess_trade_data():
        """Execute full preprocessing pipeline."""
        print(f"load_trade_data")
        df = PreProcessing.load_trade_data()
        if df is None:
            return {"message": "✅ All trade events are already preprocessed!"}

        print(f"clean_data")
        df = PreProcessing.clean_data(df)

        print(f"handle_missing_values")
        df = PreProcessing.handle_missing_values(df)

        print(f"scale_features")
        df = PreProcessing.scale_features(df)

        print(f"add_time_features")
        df = PreProcessing.add_time_features(df)

        print(f"update_pipeline_status")
        # Update MongoDB to prevent redundant preprocessing
        PreProcessing.update_pipeline_status(df["_id"].tolist())
        print("✅ Trade events successfully preprocessed and updated in MongoDB!")

        return df
