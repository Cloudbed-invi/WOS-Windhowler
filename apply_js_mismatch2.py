import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

target = '    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\n"'
replacement = target + '\n    js_content += f"const ADJACENT_MISMATCHES = {json.dumps(adjacent_mismatches)};\\n"'
code = code.replace(target, replacement)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
