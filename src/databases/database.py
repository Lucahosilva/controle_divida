import os
import pymongo

from src.utils.logger import logger


class Database:
    def __init__(self):
        self.db_password = os.getenv("MONGO_PASSWORD")
        self.db_user = os.getenv("MONGO_USER")
        self.db_host = os.getenv("MONGO_HOST")

    def _connect(self):
        logger.info("Connecting to MongoDB")
        mongo_client = pymongo.MongoClient(
            f"mongodb+srv://{self.db_user}:{self.db_password}@{self.db_host}"
        )
        db = mongo_client["Divida"]
        return db["Carro"]
