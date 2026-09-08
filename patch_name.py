import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove Name extraction logic
code = re.sub(r'name = "Unknown"\s+if "Overview" in full_text.*?except:\s*pass', '', code, flags=re.DOTALL)
code = re.sub(r'name = name\.replace.*?else name', '', code)

# 2. Update entry dict
code = code.replace(
    'entry = {"Name": name, "Level": level, "Percent": percent, "Damage": damage, "File": filename}',
    'entry = {"Level": level, "Percent": percent, "Damage": damage, "File": filename}'
)

# 3. Update writer fieldnames if missing file is being created
code = code.replace(
    'fieldnames=["File","Name","Level","Percent","Damage","Confidence","Flag_Reason"]',
    'fieldnames=["File","Level","Percent","Damage","Confidence","Flag_Reason"]'
)
code = code.replace(
    '"File": filename, "Name": name, "Level": level, "Percent": percent, \n                            "Damage": damage',
    '"File": filename, "Level": level, "Percent": percent, \n                            "Damage": damage'
)

# 4. Remove Name from raw_data export to JS
code = code.replace(
    "raw_data = df[['Level', 'Percent', 'Damage', 'Name']].to_dict(orient='records')",
    "raw_data = df[['Level', 'Percent', 'Damage']].to_dict(orient='records')"
)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    dashboard = f.read()
    
# Update dashboard saving logic
old_save = """writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": row.get("Name", "Community"),
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"])
                        })"""

new_save = """writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"]) # Keep Name in header for backward compatibility with existing csv
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": "Anonymous",
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"])
                        })"""

dashboard = dashboard.replace(old_save, new_save)
with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(dashboard)
