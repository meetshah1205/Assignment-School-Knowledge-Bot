import chromadb
from chromadb import Client
from chromadb.config import Settings

# Initialize the Chroma client
client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

# Create or retrieve the collection
try:
    collection = client.get_collection("school_content")
except chromadb.errors.InvalidCollectionException:
    collection = client.create_collection("school_content")
