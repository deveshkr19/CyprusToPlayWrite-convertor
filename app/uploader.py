import streamlit as st

def upload_file():
    uploaded_file = st.file_uploader("Upload a Cypress test file (.js or .ts)", type=["js", "ts"])
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
        st.subheader("Original Cypress Code")
        st.code(code, language="javascript")
        return code, uploaded_file.name
    return None, None
