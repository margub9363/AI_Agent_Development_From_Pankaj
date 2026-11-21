import chromadb

# Connect to ChromaDB running in Docker
client = chromadb.HttpClient(host="localhost", port=8080)

# Create a collection, or open it if it already exists
collection = client.get_or_create_collection("my_collection")

# Insert a sample record with an explicit embedding
collection.upsert(
    ids=["example-1"],
    documents=["Hello from my Day12 Python application!"],
    metadatas=[{"source": "chroma_test.py"}],
    embeddings=[[0.1, 0.2, 0.3]],
)

print(collection.get())