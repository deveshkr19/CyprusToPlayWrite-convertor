import faiss
import json
import pickle
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-mpnet-base-v2")

def rebuild_index():
    with open("knowledge_base/examples.json", "r") as f:
        examples = json.load(f)

    texts = [e["cypress"] for e in examples]
    vectors = embedder.encode(texts)
    dimension = vectors[0].shape[0]

    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    faiss.write_index(index, "knowledge_base/kb_index.faiss")
    with open("knowledge_base/kb_metadata.pkl", "wb") as f:
        pickle.dump(examples, f)

    print("✅ FAISS index rebuilt successfully.")
