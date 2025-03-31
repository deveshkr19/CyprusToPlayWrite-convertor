import streamlit as st

def show_layout():
    st.write(
        """
### 🔹 About This App
This app helps you **convert Cypress test scripts into Playwright scripts** using AI and your own project context.

### How It Works:
1. Upload a Cypress test file (.js or .ts)  
2. Click Convert – AI generates a Playwright version  
3. Edit it if needed  
4. Use the chat to improve results  
5. Save feedback to help the model learn  
"""
    )
