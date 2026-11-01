# from retriever import load_docuemtns
from retriever import retreieve

# documents = load_docuemtns()
# for name, text in documents.items():
#     print(f"Document: {name}")
#     print(f"Text: {text}")
#     print("--------------------------------")


filename, content = retreieve("python")
print(f"Filename: {filename}")
print(f"Content: {content}")