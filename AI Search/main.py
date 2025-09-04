from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests


INDEX_PATH = "index.faiss"
DOC_IDS_PATH = "doc_ids.npy"
model = SentenceTransformer('all-MiniLM-L6-v2')

app = FastAPI(
    title="AI Document Search",
    description="Local FAISS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(q:str = Query(..., description="search term")):
    index = faiss.read_index(INDEX_PATH)
    docs = np.load(DOC_IDS_PATH, allow_pickle=True)
    query_vector = model.encode([q])
    distances, indixes = index.search(query_vector, k=7)
    results = [docs[i] for i in indixes[0]]
    return results