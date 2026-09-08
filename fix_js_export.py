import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the specific JS export block
old_block = """    js_content = f"const LAST_UPDATED = '{last_updated}';\\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\\n" """

new_block = """    js_content = f"const LAST_UPDATED = '{last_updated}';\\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\\n"
    js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\\n" """

# Because of exact spacing, let's just use regex
code = re.sub(r'js_content \+= "const EXACT_LEVELS = " \+ json\.dumps\(all_levels, indent=2\) \+ ";\\n"',
              f'js_content += f"const TIER_BOUNDARIES = {{json.dumps(tier_boundaries)}};\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"\n    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"',
              code)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
