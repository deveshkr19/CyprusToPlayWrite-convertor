import faiss
import json
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-mpnet-base-v2")

def build_index():
    with open("knowledge_base/examples.json", "r") as f:
        examples = json.load(f)
    texts = [e["cypress"] for e in examples]
    vectors = embedder.encode(texts)
    dim = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index, examples

def retrieve_context(query, k=3):
    index, examples = build_index()
    query_vec = embedder.encode([query])
    distances, indices = index.search(query_vec, k)
    results = []
    for i, dist in zip(indices[0], distances[0]):
        results.append({
            "cypress": examples[i]["cypress"],
            "playwright": examples[i]["playwright"],
            "score": round(float(dist), 4)
        })
    return results
