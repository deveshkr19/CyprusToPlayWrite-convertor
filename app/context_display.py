import streamlit as st
from knowledge_base.retriever import retrieve_context

def show_kb_context(cypress_code: str) -> str:
    with st.spinner("🔍 Retrieving project context..."):
        context_data = retrieve_context(cypress_code)
    formatted = "\n\n".join([f"Cypress: {c['cypress']}\nPlaywright: {c['playwright']} (Score: {c['score']})" for c in context_data])
    st.subheader("📚 Retrieved Project Context (Knowledge Base)")
    st.code(formatted, language="text")
    return formatted
