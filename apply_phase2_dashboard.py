import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_check = """                # AI Curve Sanity Check (Power Law: 844.19 * L^4.0878)
                start = 844.19 * (lvl ** 4.0878)
                next_start = 844.19 * ((lvl + 1) ** 4.0878)
                expected = start + (pct / 100.0) * (next_start - start)
                
                error_margin = abs(dmg - expected) / expected
                if error_margin > 0.15:  # If the entry deviates by > 15% from the global model, flag it as anomaly
                    anomalies.append({
                        "Level": lvl,
                        "Percent": pct,
                        "Damage": dmg,
                        "Expected": expected,
                        "Error": error_margin
                    })
                    continue"""

new_check = """                # Tier-Aware AI Curve Sanity Check
                import wos_pipeline
                expected_start, is_prov, is_fallback = wos_pipeline.get_expected_damage(lvl)
                expected_next, _, _ = wos_pipeline.get_expected_damage(lvl + 1)
                expected = expected_start + (pct / 100.0) * (expected_next - expected_start)
                
                error_margin = abs(dmg - expected) / expected
                tolerance = 0.50 if (is_prov or is_fallback) else 0.15
                
                if error_margin > tolerance:
                    status_str = "Provisional/Fallback" if (is_prov or is_fallback) else "Confirmed Tier"
                    anomalies.append({
                        "Level": lvl,
                        "Percent": pct,
                        "Damage": dmg,
                        "Expected": expected,
                        "Error": error_margin,
                        "Reason": f"{status_str} > {int(tolerance*100)}%"
                    })
                    continue"""

code = code.replace(old_check, new_check)

# The display table for anomalies in the dashboard doesn't have a "Reason" column by default, let's just make sure it displays cleanly or doesn't crash if columns changed. st.dataframe handles dicts fine.

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
