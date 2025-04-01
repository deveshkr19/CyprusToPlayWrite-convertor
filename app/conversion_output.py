import streamlit as st
from ai_utils.conversion import convert_to_playwright, improve_with_feedback, auto_save_chat_feedback
from app.chat_interface import chat_with_model
from datetime import datetime
from pathlib import Path
import os

def show_conversion_output(cypress_code: str, context: str, original_filename: str):
    playwright_code = convert_to_playwright(cypress_code, context)

    st.subheader("✅ Converted Playwright Code")
    st.code(playwright_code, language="typescript")

    edited_code = st.text_area("✍️ Review & Edit the Converted Playwright Code", value=playwright_code, height=300)

    if edited_code != playwright_code:
        st.success("✅ You edited the generated output.")

        if st.button("🔁 Improve via Feedback Loop"):
            refined_code = improve_with_feedback(cypress_code, edited_code, context)
            st.subheader("🔁 Refined Playwright Code (AI Enhanced)")
            st.code(refined_code, language="typescript")

        if st.button("💾 Save as New Example in Knowledge Base"):
            save_feedback_to_kb(cypress_code, edited_code)
            st.success("✅ Saved to Knowledge Base!")

    os.makedirs("converted", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = original_filename.replace(".js", "").replace(".ts", "") + f"_playwright_{timestamp}.spec.ts"
    output_path = Path("converted") / output_filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(edited_code)

    with open(output_path, "rb") as f:
        st.download_button("📥 Download Converted File", data=f, file_name=output_filename)

    # Launch the chat assistant UI
    chat_with_model(cypress_code, edited_code, context)
