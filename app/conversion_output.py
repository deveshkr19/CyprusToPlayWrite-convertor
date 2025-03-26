import streamlit as st
from ai_utils.conversion import convert_to_playwright
from datetime import datetime
from pathlib import Path
import os

def show_conversion_output(cypress_code: str, context: str, original_filename: str):
    with st.spinner("⚙️ Converting using AI..."):
        playwright_code = convert_to_playwright(cypress_code)

    st.subheader("✅ Converted Playwright Code")
    st.code(playwright_code, language="typescript")

    # Save file
    os.makedirs("converted", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = original_filename.replace(".js", "").replace(".ts", "") + f"_playwright_{timestamp}.spec.ts"
    output_path = Path("converted") / output_filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(playwright_code)

    with open(output_path, "rb") as f:
        st.download_button("📥 Download Converted File", data=f, file_name=output_filename)
    st.markdown("<br><hr><p style='text-align:center;'>Developed by Devesh Kumar</p>", unsafe_allow_html=True)    