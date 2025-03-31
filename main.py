import os
import sys

# Add root directory to sys.path for app module resolution
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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
