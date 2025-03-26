from ai_utils.openai_client import get_gpt_response

def convert_to_playwright(cypress_code: str, context: str) -> str:
    prompt = f"""
You are a senior automation engineer. Convert Cypress tests to Playwright using '@playwright/test'.

Refer to these project-specific examples:
{context}

Now convert this Cypress test:
{cypress_code}

Return only the converted Playwright test code.
"""
    return get_gpt_response(prompt)

def improve_with_feedback(original_cypress, user_edited_code, context):
    prompt = f"""
You previously converted this Cypress test to Playwright:

Cypress:
{original_cypress}

User-Edited Playwright Code:
{user_edited_code}

Here are the project-specific examples:
{context}

Refine the Playwright code based on the feedback. Return only the final version.
"""
    return get_gpt_response(prompt)

def save_feedback_to_kb(cypress_code, edited_playwright_code):
    import json
    from knowledge_base.builder import rebuild_index

    new_example = {"cypress": cypress_code, "playwright": edited_playwright_code}

    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)
        data.append(new_example)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    # Automatically rebuild FAISS index after saving
    rebuild_index()
