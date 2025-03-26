import streamlit as st
from app.layout import setup_layout
from app.uploader import handle_upload
from app.context_display import show_kb_context
from app.conversion_output import show_conversion_output

setup_layout()
cypress_code, filename = handle_upload()
if cypress_code:
    context_snippet = show_kb_context(cypress_code)
    show_conversion_output(cypress_code, context_snippet, filename)
