import json
import pandas as pd

df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
print("--- RAW DATA IN CSV ---")
counts = df['Level'].value_counts().sort_index()
for lvl, count in counts.items():
    print(f"Level {lvl}: {count} data points")

print("\n--- CONFIRMED LEVELS IN exact_levels.js ---")
with open("exact_levels.js", "r", encoding="utf-8") as f:
    content = f.read()
    # Extract the JSON part
    json_str = content.split("const EXACT_LEVELS = ")[1].split(";\nconst RAW_DATA")[0]
    levels = json.loads(json_str)
    for lvl, data in levels.items():
        if data.get("confirmed", False):
            print(f"Level {lvl} is CONFIRMED")
