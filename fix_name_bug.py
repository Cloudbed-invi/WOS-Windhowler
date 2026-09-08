with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the specific block
old_entry = """                entry = {
                    "File": filename,
                    "Name": name, 
                    "Level": level, 
                    "Percent": percent, 
                    "Damage": damage, 
                    "Confidence": round(avg_conf, 3),
                    "Flag": flag_reason
                }"""

new_entry = """                entry = {
                    "File": filename,
                    "Level": level, 
                    "Percent": percent, 
                    "Damage": damage, 
                    "Confidence": round(avg_conf, 3),
                    "Flag": flag_reason
                }"""

code = code.replace(old_entry, new_entry)

# Just to be safe, also check setup_folders for Name header
code = code.replace('"File,Name,Level,Percent,Damage,Confidence,Flag_Reason\\n"', '"File,Level,Percent,Damage,Confidence,Flag_Reason\\n"')

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
