from ai_utils.openai_client import get_gpt_response

def convert_to_playwright(cypress_code: str, context: str) -> str:
    prompt = f"""
You are a senior automation engineer. Convert Cypress tests to Playwright using '@playwright/test'.

⚠️ Important rules:
- If the Cypress test fills a password field (e.g., input[name=password]), mask the value as '********' in Playwright.
- Do NOT include any real passwords in the output.

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
    import json
    from knowledge_base.builder import rebuild_index

    new_example = {
        "cypress": cypress_code,
        "playwright": edited_playwright_code,
        "rule": "user_feedback"
    }

    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)
        data.append(new_example)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    rebuild_index()
