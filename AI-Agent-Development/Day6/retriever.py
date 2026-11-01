from pathlib import Path

def load_docuemtns():
    documents = {}
    folder = Path("knowledge")
    for file in folder.glob("*.txt"):
        documents[file.name] = file.read_text(encoding="utf-8")
    return documents

def retreieve(question):
    documents = load_docuemtns()
    question = question.lower()
    for filename, content in documents.items():
        if question in content.lower():
            return filename, content
    return None, None
