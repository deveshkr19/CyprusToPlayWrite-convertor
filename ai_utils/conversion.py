from ai_utils.openai_client import get_gpt_response
import json
from knowledge_base.builder import rebuild_index


def convert_to_playwright(cypress_code: str, context: str) -> str:
    prompt = f"""
You are a senior automation engineer. Convert Cypress tests to Playwright using '@playwright/test'.

⚠️ Important rules:
- If the Cypress test fills a password field or username field, mask the value as '********' in Playwright.
- Do NOT include any real credentials in the output.

Here are project-specific examples:
{context}

Convert this Cypress test to Playwright:
{cypress_code}

Return only the Playwright test code.
"""
    return get_gpt_response(prompt)


def improve_with_feedback(original_cypress, user_edited_code, context, user_prompt=None):
    prompt = f"""
You previously converted this Cypress test to Playwright:

Cypress:
{original_cypress}

User-Edited Playwright Code:
{user_edited_code}

Examples to reference:
{context}

Now respond to the user's request:
{user_prompt}

Return the improved Playwright code.
"""
    return get_gpt_response(prompt)


def save_feedback_to_kb(cypress_code, edited_playwright_code):
    new_example = {
        "cypress": cypress_code.strip(),
        "playwright": edited_playwright_code.strip(),
        "rule": "user_feedback"
    }

    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)
        data.append(new_example)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    rebuild_index()


def auto_save_chat_feedback(cypress_code, generated_playwright_code):
    rule = "user_feedback"
    if "fill('********')" in generated_playwright_code and "#username" in cypress_code:
        rule = "mask_username"

    new_example = {
        "cypress": cypress_code.strip(),
        "playwright": generated_playwright_code.strip(),
        "rule": rule
    }

    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)
        # Avoid duplicates
        if any(e["cypress"] == new_example["cypress"] and e["playwright"] == new_example["playwright"] for e in data):
            return
        data.append(new_example)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    rebuild_index()
