from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.embeddings.create(
    model="nomic-embed-text",
    input="Python is a programming language."
)

embedding = response.data[0].embedding
print(type(embedding))
print(len(embedding))
print(embedding)