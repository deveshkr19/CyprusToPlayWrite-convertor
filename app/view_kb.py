import streamlit as st
import json

def view_knowledge_base():
    st.subheader("📘 Knowledge Base Entries")
    try:
        with open("knowledge_base/examples.json", "r") as f:
            examples = json.load(f)

        if not examples:
            st.info("Your knowledge base is currently empty.")
            return

        # Show last 5 examples (most recent first)
        for ex in examples[-5:][::-1]:
            st.code(
                f"Cypress: {ex['cypress']}\nPlaywright: {ex['playwright']}\nRule: {ex.get('rule', 'N/A')}",
                language="text"
            )
    except FileNotFoundError:
        st.warning("Knowledge base file not found.")
    except json.JSONDecodeError:
        st.error("Failed to load knowledge base: Invalid JSON format.")
