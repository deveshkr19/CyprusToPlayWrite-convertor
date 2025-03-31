import streamlit as st
from app.layout import show_layout
from app.uploader import upload_file
from app.context_display import show_kb_context
from app.conversion_output import show_conversion_output

st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")

st.title("🧪 Cypress to Playwright Converter using Gen AI")

show_layout()

uploaded_file = upload_file()

if uploaded_file:
    cypress_code = uploaded_file.read().decode("utf-8")
    st.subheader("📄 Original Cypress Code")
    st.code(cypress_code, language="javascript")

    # Retrieve examples from FAISS + rule-based context
    context_snippet = show_kb_context(cypress_code)

    # Show AI-generated Playwright conversion and chat-based refinements
    show_conversion_output(cypress_code, context_snippet, uploaded_file.name)
