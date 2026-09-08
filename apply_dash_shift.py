import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_dash = """                if t_status == "EXTRAPOLATED":
                    item["Reason"] = f"No tier fit for level {lvl} - manual review required"
                    flagged.append(item)
                elif error_margin > tol:
                    tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                    item["Reason"] = f"{tier_name} tier: {error_margin*100:.1f}% deviation exceeds {int(tol*100)}% threshold"
                    flagged.append(item)
                else:
                    valid.append(item)"""

new_dash = """                if t_status == "EXTRAPOLATED":
                    item["Reason"] = f"No tier fit for level {lvl} - manual review required"
                    flagged.append(item)
                elif error_margin > tol:
                    tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                    item["Reason"] = f"{tier_name} tier: {error_margin*100:.1f}% deviation exceeds {int(tol*100)}% threshold"
                    flagged.append(item)
                else:
                    # Window Shift Check
                    shift = 0.0
                    if t_status == "CONFIRMED":
                        try:
                            shift = wos_pipeline.check_window_shift(lvl, pct, dmg)
                        except:
                            pass
                    
                    if shift > 0.05:
                        item["Reason"] = f"window shift: {shift*100:.1f}% - possible different account"
                        flagged.append(item)
                    else:
                        valid.append(item)"""

code = code.replace(old_dash, new_dash)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
