import streamlit as st
import json

def debug_kb_viewer():
    st.title("🔍 Debug: Full Raw Knowledge Base Viewer")

    try:
        with open("knowledge_base/examples.json", "r") as f:
            examples = json.load(f)

        st.markdown(f"**Total Examples:** {len(examples)}")

        for idx, ex in enumerate(reversed(examples)):
            st.markdown(f"### Entry #{len(examples) - idx}")
            st.json(ex)

    except FileNotFoundError:
        st.error("❌ examples.json file not found.")
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format in examples.json.")
