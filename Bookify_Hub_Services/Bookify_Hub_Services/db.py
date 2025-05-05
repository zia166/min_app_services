from django.conf import settings
from pymongo import MongoClient
import certifi

client = MongoClient(
    settings.ATLAS_CONNECTION_STRING,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=False,
    tlsAllowInvalidHostnames=False,
    retryWrites=True,
    w='majority'
)

# Connect to MongoDB
dbconn = client[settings.MONGO_DB]
