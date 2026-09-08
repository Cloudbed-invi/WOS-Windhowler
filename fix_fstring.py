with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix f-string again (Powershell string interpolation escaping issues)
code = code.replace(
    'js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"\n    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"',
    'js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\\\n"\n    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\\\n"'
)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
