from ai_utils.openai_client import get_gpt_response
import json
from knowledge_base.builder import rebuild_index
import logging

logging.basicConfig(level=logging.INFO)

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


def auto_save_chat_feedback(cypress_code, generated_playwright_code):
    from knowledge_base.builder import rebuild_index
    import json
    import re

    new_examples = []

    # Split into lines for matching
    cypress_lines = [line.strip() for line in cypress_code.splitlines() if "cy.get" in line and ".type(" in line]
    playwright_lines = [line.strip() for line in generated_playwright_code.splitlines() if "page.locator" in line and ".fill(" in line]

    # Match lines by index (assumes order is preserved)
    for c_line, p_line in zip(cypress_lines, playwright_lines):
        rule = "user_feedback"
        if "password" in c_line or "password" in p_line:
            rule = "mask_password"
        elif "username" in c_line or "username" in p_line:
            rule = "mask_username"

        new_example = {
            "cypress": c_line,
            "playwright": p_line,
            "rule": rule
        }

        new_examples.append(new_example)

    # Read existing examples.json
    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)

        for example in new_examples:
            exists = any(
                e["cypress"] == example["cypress"] and e["playwright"] == example["playwright"]
                for e in data
            )
            if not exists:
                data.append(example)
                print("💾 New KB entry saved:", example)

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    # Rebuild FAISS index
    rebuild_index()
