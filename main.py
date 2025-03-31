import streamlit as st
from app.layout import show_layout
from app.uploader import upload_file  # <- make sure uploader.py has: def upload_file()
from app.context_display import show_kb_context
from app.conversion_output import show_conversion_output

# Configure Streamlit page
st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")
st.title("🧪 Cypress to Playwright Converter using Gen AI")

# Show layout description
show_layout()

# Handle file upload
cypress_code, file_name = upload_file()

if cypress_code:
    # Get examples from knowledge base + FAISS + rules
    context_snippet = show_kb_context(cypress_code)

    # Show conversion output + chat + feedback saving
    show_conversion_output(cypress_code, context_snippet, file_name)
