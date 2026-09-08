with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# I will just write a python script to redefine adjacent_mismatches earlier or move it up.
import re

start_idx = code.find("    js_content = f\"const LAST_UPDATED")
end_idx = code.find("        f.write(js_content)") + len("        f.write(js_content)")

js_block = code[start_idx:end_idx]
code = code[:start_idx] + code[end_idx:]

insert_idx = code.find("    formulas_config = {")
code = code[:insert_idx] + js_block + "\n\n" + code[insert_idx:]

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
