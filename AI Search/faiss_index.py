import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import fitz

DOCS_FOLDER = "docs"
INDEX_PATH = "index.faiss"
DOC_IDS_PATH = "doc_ids.npy"

model = SentenceTransformer('all-MiniLM-L6-v2')

def split_chunks(text:str,chunck_size:int=500,overlap:int=50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunck_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunck_size - overlap
    return chunks

def load_documents() -> List[str]:
    docs = []
    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".pdf"):
            with fitz.open(os.path.join(DOCS_FOLDER, filename)) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                docs.append(text)
        if text.strip():
            chunks = split_chunks(text, 500, 50)
            docs.extend(chunks)
    return docs

def build_index():
    documents = load_documents()
    embeddings = model.encode(documents, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    np.save(DOC_IDS_PATH, np.array(documents))
    print("✔️ Index Built")

if __name__ == "__main__":
    build_index()

