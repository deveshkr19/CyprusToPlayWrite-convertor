import faiss
import pickle
import json
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(json_file_path="knowledge_base/examples.json"):
    with open(json_file_path, "r") as f:
        examples = json.load(f)
    
    texts = [e["cypress"] for e in examples]
    vectors = embedder.encode(texts)
    
    index = faiss.IndexFlatL2(vectors[0].shape[0])
    index.add(vectors)

    with open("knowledge_base/kb_metadata.pkl", "wb") as f:
        pickle.dump(examples, f)
    faiss.write_index(index, "knowledge_base/kb_index.faiss")
