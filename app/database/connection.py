
import os
from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv # type: ignore
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
