import faiss
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

# Paths to files inside knowledge_base folder
EXCEL_PATH = "knowledge_base/Cypress&PlaywrightCode.xlsx"
JSON_PATH = "knowledge_base/examples.json"

# Initialize SentenceTransformer embedder
embedder = SentenceTransformer("all-mpnet-base-v2")

# Load examples from the Excel file
def load_examples_from_excel():
    df = pd.read_excel(EXCEL_PATH,engine="openpyxl")
    st.write(f"✅ Loaded {len(df)} rows from Excel KB")

    examples = []

    for _, row in df.iterrows():
        cypress = str(row.get("Cypress", "")).strip()
        playwright = str(row.get("Playwright", "")).strip()
        if cypress and playwright:
            examples.append({
                "cypress": cypress,
                "playwright": playwright
            })
    return examples

# Load examples from both Excel and JSON
def load_examples():
    json_examples = []
    try:
        with open(JSON_PATH, "r") as f:
            json_examples = json.load(f)
    except FileNotFoundError:
        pass

    excel_examples = load_examples_from_excel()
    return json_examples + excel_examples

# Build FAISS index from examples
def build_index():
    examples = load_examples()
    st.write(f"📊 Total examples indexed: {len(examples)}")
    texts = [e["cypress"] for e in examples]
    vectors = embedder.encode(texts)
    dim = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index, examples

# Retrieve top-k similar Cypress examples
def retrieve_context(query, k=3):
    index, examples = build_index()
    query_vec = embedder.encode([query])
    distances, indices = index.search(query_vec, k)

    results = [
        {
            "cypress": examples[i]["cypress"],
            "playwright": examples[i]["playwright"],
            "score": round(float(dist), 4)
        }
        for i, dist in zip(indices[0], distances[0])
    ]

    # Rule-based injection logic
    rule_based = []
    for ex in examples:
        if ex.get("rule") in ["user_feedback", "mask_username"] and "#username" in query:
            rule_based.append({
                "cypress": ex["cypress"],
                "playwright": ex["playwright"],
                "score": 1.0
            })

    return results + rule_based
