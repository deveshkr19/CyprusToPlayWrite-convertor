import streamlit as st
from app.layout import setup_layout
from app.uploader import handle_upload
from app.context_display import show_kb_context
from app.conversion_output import show_conversion_output

# Page setup and branding
setup_layout()

# Upload and read Cypress test
cypress_code, filename = handle_upload()

if cypress_code:
    # Step 1: Show retrieved project context
    context_snippet = show_kb_context(cypress_code)

    # Step 2: Convert & show output
    show_conversion_output(cypress_code, context_snippet, filename)
