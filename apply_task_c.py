with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update wos_pipeline.py signature
code = code.replace("def run_ocr(progress_callback=None):", "def run_ocr(progress_callback=None, write_to_csv=True):")

# 2. Update needs_review.csv logic
old_flag = """                # If automated CLI is running, separate them. If dashboard, dashboard handles it.
                if flag_reason:
                    with open("needs_review.csv", mode='a', newline='', encoding='utf-8') as f:"""
new_flag = """                # If automated CLI is running, separate them. If dashboard, dashboard handles it.
                if flag_reason and write_to_csv:
                    with open("needs_review.csv", mode='a', newline='', encoding='utf-8') as f:"""
code = code.replace(old_flag, new_flag)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()
    
code = code.replace("new_entries = wos_pipeline.run_ocr(progress_callback=update_progress)", "new_entries = wos_pipeline.run_ocr(progress_callback=update_progress, write_to_csv=False)")

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
