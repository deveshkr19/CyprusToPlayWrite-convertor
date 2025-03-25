import faiss
import pickle
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, k=2):
    index = faiss.read_index("knowledge_base/kb_index.faiss")
    with open("knowledge_base/kb_metadata.pkl", "rb") as f:
        examples = pickle.load(f)

    vector = embedder.encode([query])
    _, indices = index.search(vector, k)

    results = [examples[i]["cypress"] + " => " + examples[i]["playwright"] for i in indices[0]]
    return "\n".join(results)
    