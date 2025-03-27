def auto_save_chat_feedback(cypress_code, generated_playwright_code):
    import json
    from knowledge_base.builder import rebuild_index

    # Basic rule detection (optional expansion)
    rule = "user_feedback"
    if "fill('********')" in generated_playwright_code and "#username" in cypress_code:
        rule = "mask_username"

    new_example = {
        "cypress": cypress_code,
        "playwright": generated_playwright_code,
        "rule": rule
    }

    with open("knowledge_base/examples.json", "r+") as f:
        data = json.load(f)

        # Avoid duplicates
        for e in data:
            if e["cypress"] == new_example["cypress"] and e["playwright"] == new_example["playwright"]:
                return  # Already saved

        data.append(new_example)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    rebuild_index()
