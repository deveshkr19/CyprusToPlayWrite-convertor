import faiss
import pickle
import json
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def build_index():
    with open("knowledge_base/examples.json", "r") as f:
        examples = json.load(f)

    texts = [e["cypress"] for e in examples]
    vectors = embedder.encode(texts)

    dimension = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    return index, examples

def retrieve_context(query, k=2):
    index, examples = build_index()
    query_vector = embedder.encode([query])
    _, indices = index.search(query_vector, k)

    results = [
        f"{examples[i]['cypress']} => {examples[i]['playwright']}"
        for i in indices[0]
    ]
    return "\n".join(results)
