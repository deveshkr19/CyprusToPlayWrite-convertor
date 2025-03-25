import streamlit as st
from ai_utils.conversion import convert_to_playwright
from datetime import datetime
from pathlib import Path
import os

st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")
st.title("🚀 Cypress to Playwright Converter using Gen AI")

st.write("""
### 🔹 About This App
This tool converts **Cypress test scripts** to **Playwright** using AI and project-specific examples.
""")

uploaded_file = st.file_uploader("Upload Cypress test file (.js or .ts)", type=["js", "ts"])

if uploaded_file:
    cypress_code = uploaded_file.read().decode("utf-8")
    st.subheader("📜 Original Cypress Code")
    st.code(cypress_code, language="javascript")

    with st.spinner("Converting..."):
        playwright_code = convert_to_playwright(cypress_code)

    st.subheader("✅ Converted Playwright Code")
    st.code(playwright_code, language="typescript")

    # Save file
    os.makedirs("converted", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = uploaded_file.name.replace(".js", "").replace(".ts", "") + f"_playwright_{timestamp}.spec.ts"
    path = Path("converted") / filename

    with open(path, "w") as f:
        f.write(playwright_code)

    with open(path, "rb") as f:
        st.download_button("📥 Download Converted File", data=f, file_name=filename)
