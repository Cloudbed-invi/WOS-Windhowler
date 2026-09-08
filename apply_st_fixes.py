import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix use_container_width
code = code.replace("use_container_width=True", "width='stretch'")

# Fix Avg Confidence mixed type
old_conf_logic = """            for lvl in levels:
                d = df_data[df_data["Level"] == lvl]
                count = len(d)
                conf = d["Confidence"].mean() if (has_conf and count > 0) else "N/A"
                cov_rows.append({"Level": lvl, "Confirmed Points": count, "Avg Confidence": conf})"""

new_conf_logic = """            for lvl in levels:
                d = df_data[df_data["Level"] == lvl]
                count = len(d)
                conf = round(d["Confidence"].mean(), 3) if (has_conf and count > 0 and not d["Confidence"].isna().all()) else None
                cov_rows.append({"Level": lvl, "Confirmed Points": count, "Avg Confidence": conf})"""

code = code.replace(old_conf_logic, new_conf_logic)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
