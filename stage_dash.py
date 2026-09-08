import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_dash = """                # Tier-Aware AI Curve Sanity Check
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
                
                if error_margin <= tolerance:
                    valid.append(item)
                else:
                    status_str = "Provisional Tier/Fallback" if (is_prov or is_fallback) else "Confirmed Tier"
                    item["Reason"] = f"{status_str} > {int(tolerance*100)}%"
                    flagged.append(item)"""

new_dash = """                # Tier-Aware AI Curve Sanity Check
                import wos_pipeline
                expected_start, t_status, tol = wos_pipeline.get_expected_damage(lvl)
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
                
                if t_status == "EXTRAPOLATED":
                    item["Reason"] = f"No tier fit for level {lvl} - manual review required"
                    flagged.append(item)
                elif error_margin > tol:
                    tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                    item["Reason"] = f"{tier_name} tier: {error_margin*100:.1f}% deviation exceeds {int(tol*100)}% threshold"
                    flagged.append(item)
                else:
                    valid.append(item)"""
                    
code = code.replace(old_dash, new_dash)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
