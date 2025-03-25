import openai
import streamlit as st

# Load API key
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize client
client = openai.OpenAI(api_key=api_key)

def get_gpt_response(prompt, temperature=0.2):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content
