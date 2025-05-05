from django.conf import settings
from pymongo import MongoClient
import certifi
import ssl

client = MongoClient(
    settings.ATLAS_CONNECTION_STRING,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True,
    tlsAllowInvalidHostnames=True,
    retryWrites=True,
    w='majority',
    connectTimeoutMS=30000,
    socketTimeoutMS=30000,
    serverSelectionTimeoutMS=30000,
    ssl_cert_reqs=ssl.CERT_NONE
)

# Connect to MongoDB
dbconn = client[settings.MONGO_DB]
