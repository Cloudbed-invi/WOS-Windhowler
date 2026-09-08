import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_block = r'''                # AI Curve Sanity Check \(Power Law: 844\.19 \* L\^4\.0878\)\s+start = 844\.19 \* \(lvl \*\* 4\.0878\)\s+next_start = 844\.19 \* \(\(lvl \+ 1\) \*\* 4\.0878\)\s+expected = start \+ \(pct / 100\.0\) \* \(next_start - start\)\s+error_margin = abs\(dmg - expected\) / expected\s+item = \{\s+"Level": lvl, \s+"Percent": pct, \s+"Damage": dmg, \s+"Deviation": f"\{error_margin \* 100:\.1f\}%",\s+"Timestamp": row\['Timestamp'\]\s+\}\s+# 15% tolerance for new submissions\s+if error_margin > 0\.15:\s+anomalies\.append\(item\)'''

new_block = '''                # Tier-Aware AI Curve Sanity Check
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
                    anomalies.append(item)'''

code = re.sub(old_block, new_block, code)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
