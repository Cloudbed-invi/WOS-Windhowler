import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_js = """    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n\"""

new_js = """    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\n"
    js_content += f"const ADJACENT_MISMATCHES = {json.dumps(adjacent_mismatches)};\\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n\"""
code = code.replace(old_js, new_js)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
