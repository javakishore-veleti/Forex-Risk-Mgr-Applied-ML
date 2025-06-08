from pymongo import MongoClient
import threading


class MongoDBConnFacade:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, db_name="forex_risk_mgr_db", host="localhost", port=27017):
        """Private constructor to prevent direct instantiation."""
        if MongoDBConnFacade._instance is not None:
            raise Exception("Use getInstance() method to get an instance.")
        self.client = MongoClient(f"mongodb://{host}:{port}/")
        self.db = self.client[db_name]

    @classmethod
    def getInstance(cls, db_name="forex_risk_mgr_db", host="localhost", port=27017):
        """Ensures only one instance of MongoDBConnFacade exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(db_name, host, port)
        return cls._instance

    def is_collection_empty(self, collection_name):
        """Check if a MongoDB collection is empty."""
        return self.db[collection_name].count_documents({}) == 0

    def save(self, collection_name, data):
        """Save a single document or multiple documents."""
        collection = self.db[collection_name]
        return collection.insert_many(data) if isinstance(data, list) else collection.insert_one(data)

    def get(self, collection_name, query={}):
        """Retrieve documents based on a query."""
        return self.db[collection_name].find(query)

    def get_all(self, collection_name):
        """Retrieve all documents."""
        return self.db[collection_name].find({})

    def find_by_id(self, collection_name, doc_id):
        """Find document by ID."""
        return self.db[collection_name].find_one({"_id": doc_id})

    def find_by_criteria(self, collection_name, criteria):
        """Find documents based on custom criteria."""
        return self.db[collection_name].find(criteria)

    def delete(self, collection_name, query):
        """Delete document(s) based on query."""
        return self.db[collection_name].delete_many(query)

    def close_connection(self):
        """Close MongoDB connection."""
        self.client.close()
