import streamlit as st
from ai_utils.conversion import improve_with_feedback, save_feedback_to_kb

def chat_with_model(cypress_code, edited_code, context):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("💬 Chat with the Conversion Assistant")

    # Display chat history
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["message"])

    # Chat input
    user_prompt = st.chat_input("Ask me to improve or update the Playwright code...")

    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "message": user_prompt})

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            response = improve_with_feedback(
                original_cypress=cypress_code,
                user_edited_code=edited_code,
                context=context,
                user_prompt=user_prompt
            )
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "message": response})

        if st.button("💾 Save this AI-improved version to Knowledge Base"):
            save_feedback_to_kb(cypress_code, response)
            st.success("✅ Saved to Knowledge Base!")
