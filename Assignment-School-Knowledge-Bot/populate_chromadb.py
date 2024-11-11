from chromadb import Client
from chromadb.config import Settings

# Initialize ChromaDB client with updated settings
client = Client(Settings(
    chroma_db_impl="duckdb+parquet",  # Use updated database configuration
    persist_directory="./chroma_db"  # Directory to store the database
))


# Sample data setup for ChromaDB - replace this with your actual logic
# Assuming a sample function to populate the database for demonstration

def populate_database():
    # Replace with the actual collection and data insertion logic
    collection = client.create_collection("example_collection")

    # Sample data, replace this with your own data to insert
    collection.add(documents=[
        {"id": "1", "content": "Sample document 1"},
        {"id": "2", "content": "Sample document 2"}
    ])
    print("Database populated with sample data.")


# Run the population script
populate_database()
