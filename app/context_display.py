import streamlit as st
from knowledge_base.retriever import retrieve_context

def show_kb_context(cypress_code: str) -> str:
    context_data = retrieve_context(cypress_code)
    
    st.subheader("📚 Retrieved Project Context (Knowledge Base)")
    context_str = ""
    for item in context_data:
        cypress = item['cypress']
        playwright = item['playwright']
        score = item.get("score", 1.0)
        snippet = f"Cypress: {cypress}\nPlaywright: {playwright} (Score: {score})\n"
        context_str += snippet
        st.code(snippet, language="text")
    
    return context_str
