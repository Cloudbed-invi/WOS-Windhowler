import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update the manual approval of OCR data block
old_approve = """        if st.button("✅ Approve & Publish to AI Model", type="primary"):
            # Save approved data to CSV (ignoring Confidence/Flag columns to keep master data pure)
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"]) # Keep Name in header for backward compatibility with existing csv
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": "Anonymous",
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"])
                        })"""

new_approve = """        if st.button("✅ Approve & Publish to AI Model", type="primary"):
            # Save approved data to CSV (now preserving Confidence per user request)
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"]) # Added Confidence
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": "Anonymous",
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"]),
                            "Confidence": row.get("Confidence", "")
                        })"""
code = code.replace(old_approve, new_approve)

# 2. Update the flagged reads approval block
old_flag = """                    if st.button("Approve", key=f"app_{idx}"):
                        new_row = pd.DataFrame({
                            "File": [row.get("File", "Manual")],
                            "Name": ["Community"],
                            "Level": [row["Level"]],
                            "Percent": [row["Percent"]],
                            "Damage": [row["Damage"]]
                        })
                        new_row.to_csv("data.csv", mode="a", header=not os.path.exists("data.csv"), index=False)"""

new_flag = """                    if st.button("Approve", key=f"app_{idx}"):
                        new_row = pd.DataFrame({
                            "File": [row.get("File", "Manual")],
                            "Name": ["Community"],
                            "Level": [row["Level"]],
                            "Percent": [row["Percent"]],
                            "Damage": [row["Damage"]],
                            "Confidence": [row.get("Confidence", "")]
                        })
                        new_row.to_csv("data.csv", mode="a", header=not os.path.exists("data.csv"), index=False)"""
code = code.replace(old_flag, new_flag)

# 3. Fix the top of the file so pandas to_csv matches headers.
# Actually, wait. The Google Forms write block
old_forms = """                        writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                        for v in st.session_state.form_valid:
                            writer.writerow({"File": "GoogleForm", "Name": "Community", "Level": v["Level"], "Percent": v["Percent"], "Damage": int(v["Damage"])})"""
                            
new_forms = """                        writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"])
                        for v in st.session_state.form_valid:
                            writer.writerow({"File": "GoogleForm", "Name": "Community", "Level": v["Level"], "Percent": v["Percent"], "Damage": int(v["Damage"]), "Confidence": ""})"""
code = code.replace(old_forms, new_forms)

# 4. Fix manual entry block
old_manual = """            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                writer.writerow({
                    "File": "ManualEntry", 
                    "Name": "Admin", 
                    "Level": int(man_level), 
                    "Percent": float(man_percent), 
                    "Damage": int(man_damage)
                })"""

new_manual = """            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"])
                writer.writerow({
                    "File": "ManualEntry", 
                    "Name": "Admin", 
                    "Level": int(man_level), 
                    "Percent": float(man_percent), 
                    "Damage": int(man_damage),
                    "Confidence": ""
                })"""
code = code.replace(old_manual, new_manual)


with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
