with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "                # AI Curve Sanity Check (Power Law: 844.19 * L^4.0878)" in line:
        skip = True
        new_lines.append("""                # Tier-Aware AI Curve Sanity Check
                import wos_pipeline
                expected_start, is_prov, is_fallback = wos_pipeline.get_expected_damage(lvl)
                expected_next, _, _ = wos_pipeline.get_expected_damage(lvl + 1)
                expected = expected_start + (pct / 100.0) * (expected_next - expected_start)
                
                error_margin = abs(dmg - expected) / expected
                
                item = {
                    "Level": lvl, 
                    "Percent": pct, 
                    "Damage": dmg, 
                    "Deviation": f"{error_margin * 100:.1f}%",
                    "Timestamp": row['Timestamp']
                }
                
                # Dynamic tolerance based on tier confidence
                tolerance = 0.50 if (is_prov or is_fallback) else 0.15
                if error_margin > tolerance:
                    status_str = "Provisional Tier/Fallback" if (is_prov or is_fallback) else "Confirmed Tier"
                    item["Reason"] = f"{status_str} > {int(tolerance*100)}%"
                    anomalies.append(item)
                    continue\n""")
        continue
    
    if skip:
        if "                    anomalies.append(item)" in line:
            skip_next_continue = True # need to skip the continue as well
        elif "                    continue" in line and 'skip_next_continue' in locals() and skip_next_continue:
            skip = False
        elif not line.strip() or line.strip() == "continue": # Sometimes it's right there
            if line.strip() == "continue" and "anomalies.append" in ''.join(lines[-10:]):
                pass
        continue
    
    new_lines.append(line)

# Let's do a safer block replace
with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

import re
old_regex = r"                # AI Curve Sanity Check.*?anomalies\.append\(item\)\s+continue"

new_code = """                # Tier-Aware AI Curve Sanity Check
                import wos_pipeline
                expected_start, is_prov, is_fallback = wos_pipeline.get_expected_damage(lvl)
                expected_next, _, _ = wos_pipeline.get_expected_damage(lvl + 1)
                expected = expected_start + (pct / 100.0) * (expected_next - expected_start)
                
                error_margin = abs(dmg - expected) / expected
                
                item = {
                    "Level": lvl, 
                    "Percent": pct, 
                    "Damage": dmg, 
                    "Deviation": f"{error_margin * 100:.1f}%",
                    "Timestamp": row['Timestamp']
                }
                
                # Dynamic tolerance based on tier confidence
                tolerance = 0.50 if (is_prov or is_fallback) else 0.15
                if error_margin > tolerance:
                    status_str = "Provisional Tier/Fallback" if (is_prov or is_fallback) else "Confirmed Tier"
                    item["Reason"] = f"{status_str} > {int(tolerance*100)}%"
                    anomalies.append(item)
                    continue"""

code = re.sub(old_regex, new_code, code, flags=re.DOTALL)
with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

