with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

start_marker = "                # AI Curve Sanity Check (Power Law: 844.19 * L^4.0878)"
end_marker = "                    anomalies.append(item)"

start_idx = code.find(start_marker)
end_idx = code.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    old_block = code[start_idx:end_idx]
    new_block = """                # Tier-Aware AI Curve Sanity Check
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
                    anomalies.append(item)"""
    code = code[:start_idx] + new_block + code[end_idx:]

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
