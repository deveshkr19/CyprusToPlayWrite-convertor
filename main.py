import streamlit as st
from ai_utils.conversion import convert_to_playwright
from knowledge_base.retriever import retrieve_context
from datetime import datetime
from pathlib import Path
import os

# Page settings
st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")

# Title and description
st.title("🚀 Cypress to Playwright Converter using Gen AI")

st.write("""
### 🔹 About This App
This tool converts **Cypress test scripts** to **Playwright** using AI and project-specific examples.
""")

# File uploader
uploaded_file = st.file_uploader("📤 Upload a Cypress test file (.js or .ts)", type=["js", "ts"])

# Process the uploaded file
if uploaded_file:
    cypress_code = uploaded_file.read().decode("utf-8")
    
    st.subheader("📜 Original Cypress Code")
    st.code(cypress_code, language="javascript")

    # Step 1: Retrieve context from FAISS-based knowledge base
    with st.spinner("🔍 Retrieving project context..."):
        context_snippet = retrieve_context(cypress_code)
    
    st.subheader("📚 Retrieved Project Context (Knowledge Base)")
    st.code(context_snippet, language="text")

    # Step 2: Convert using GPT with context
    with st.spinner("⚙️ Converting using AI..."):
        playwright_code = convert_to_playwright(cypress_code)

    st.subheader("✅ Converted Playwright Code")
    st.code(playwright_code, language="typescript")

    # Step 3: Save and offer download
    os.makedirs("converted", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = uploaded_file.name.replace(".js", "").replace(".ts", "") + f"_playwright_{timestamp}.spec.ts"
    path = Path("converted") / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(playwright_code)

    with open(path, "rb") as f:
        st.download_button("📥 Download Converted File", data=f, file_name=filename)
