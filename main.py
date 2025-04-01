import streamlit as st
from app.layout import show_layout
from app.uploader import upload_file
from app.context_display import show_kb_context
from app.conversion_output import show_conversion_output
from app.view_kb import view_knowledge_base
from app.debug_kb import debug_kb_viewer  # NEW

# Page config
st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")
st.title("🧪 Cypress to Playwright Converter using Gen AI")

# Description and layout
show_layout()

# File upload
cypress_code, file_name = upload_file()

# If file is uploaded
if cypress_code:
    context_snippet = show_kb_context(cypress_code)
    show_conversion_output(cypress_code, context_snippet, file_name)

    # 📘 View KB entries
    with st.expander("📚 View Recent Knowledge Base Entries"):
        view_knowledge_base()

    # 🧠 Full Debug Viewer
    with st.expander("🧠 Full Raw Knowledge Base Debug Viewer"):
        debug_kb_viewer()
