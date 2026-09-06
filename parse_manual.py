import re
import csv
import pandas as pd
import os

entries = []

# Parse raw_data1.txt
with open("raw_data1.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        # Format: 72,423,951 - 29% of trial lv. 17
        m = re.search(r'([\d,]+)\s*-\s*(\d+)%?\s*.*lv\.?\s*(\d+)', line, re.IGNORECASE)
        if m:
            dmg = int(m.group(1).replace(',', ''))
            pct = int(m.group(2))
            lvl = int(m.group(3))
            entries.append({'File': 'Manual', 'Name': 'Manual', 'Level': lvl, 'Percent': pct, 'Damage': dmg})

# Parse raw_data2.csv
with open("raw_data2.csv", "r") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        parts = line.split(',')
        if len(parts) == 3:
            lvl = int(parts[0])
            pct = int(parts[1])
            dmg = int(parts[2])
            entries.append({'File': 'Manual', 'Name': 'Manual', 'Level': lvl, 'Percent': pct, 'Damage': dmg})

# Combine with existing data.csv
if os.path.exists("data.csv"):
    df_existing = pd.read_csv("data.csv")
    existing_entries = df_existing.to_dict('records')
    entries.extend(existing_entries)

# Save merged data.csv
df_all = pd.DataFrame(entries).drop_duplicates(subset=['Level', 'Percent', 'Damage'])
df_all.to_csv("data.csv", index=False)
print(f"Total data points saved: {len(df_all)}")
