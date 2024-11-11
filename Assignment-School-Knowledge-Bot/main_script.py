from chromadb import Client
from chromadb.config import Settings

# Update Chroma client initialization
client = Client(Settings(
    persist_directory="./chroma_db"  # Directory to store the database
))


