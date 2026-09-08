import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's fix the broken f-string
code = code.replace(
    'js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"\n    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"',
    'js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\\\n"\n    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\\\n"'
)

# Actually, wait, let's just rewrite the end completely correctly.
end_marker = "    js_content = f\"const LAST_UPDATED = '{last_updated}';\\n\""
split = code.split(end_marker)
if len(split) > 1:
    code = split[0] + """    js_content = f"const LAST_UPDATED = '{last_updated}';\\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\\n"
    js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\\n"
    
    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return {
        "levels": all_levels,
        "A": extrapolate_A,
        "B": extrapolate_B
    }

if __name__ == "__main__":
    setup_folders()
    run_ml_and_export()
"""
    
with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
