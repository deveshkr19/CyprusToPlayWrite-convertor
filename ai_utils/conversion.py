from ai_utils.openai_client import get_gpt_response
from knowledge_base.retriever import retrieve_context

def convert_to_playwright(cypress_code: str) -> str:
    context = retrieve_context(cypress_code)
    prompt = f"""
You are a senior automation engineer. Convert Cypress tests to Playwright using '@playwright/test'.

Project-specific examples:
{context}

Now convert this Cypress code:

{cypress_code}

Playwright Test:
"""
    return get_gpt_response(prompt)
