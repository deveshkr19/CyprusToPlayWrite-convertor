import streamlit as st
from knowledge_base.retriever import retrieve_context

def show_kb_context(cypress_code: str) -> str:
    with st.spinner("Retrieving project context..."):
        context = retrieve_context(cypress_code)
    st.subheader("Retrieved Project Context (Knowledge Base)")
    st.code(context, language="text")
    return context
