from django.conf import settings
from pymongo import MongoClient
import certifi


client = MongoClient(settings.ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
# Connect to MongoDB
dbconn = client[settings.MONGO_DB]
