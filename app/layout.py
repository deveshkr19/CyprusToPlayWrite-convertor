import streamlit as st

def setup_layout():
    st.set_page_config(page_title="Cypress to Playwright Converter", layout="wide")
    st.title("🚀 Cypress to Playwright Converter using Gen AI")

    st.write("""
    ### 🔹 About This App
    This tool converts **Cypress test scripts** to **Playwright** using AI and project-specific examples.
    """)
