from openai import OpenAI
from dotenv import load_dotenv
import os
from retriever import load_docuemtns
from test_embedding import create_embedding
from similarity import cosine_similarity

documents = load_docuemtns()
document_embeddings = {}
for filename, content in documents.items():
    document_embeddings[filename] = create_embedding(content)

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


print("=" * 40)
print("       My AI Assistant")
print("=" * 40)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Assistant: Goodbye!")
        break

    question_embedding = create_embedding(user_input)

    best_score = -1
    best_document = None

    for filename, embedding in document_embeddings.items():
        score = cosine_similarity(question_embedding, embedding)
        if score > best_score:
            best_score = score
            best_document = filename

    context = documents[best_document]
    prompt = f"""
    Answer the question using only the following information.
    Context: {context}
    Question: {user_input}
    """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[{"role": "user", "content": prompt}]
    )
    print(response.choices[0].message.content)