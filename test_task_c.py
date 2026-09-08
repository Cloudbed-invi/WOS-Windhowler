import pandas as pd
import os
import wos_pipeline
import json
import csv

# 1. Clean slate
if os.path.exists("needs_review.csv"):
    os.remove("needs_review.csv")
    
# Create a fake image that causes a window_shift_check flag
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (800, 200), color=(255,255,255))
d = ImageDraw.Draw(img)
# Using Franco's data that triggered the window shift
d.text((10,10), "Lv. 25 reaching 67% dealt 434,683,450 damage", fill=(0,0,0))
img.save("images/fake_franco.png")

print("=== Needs Review Before OCR ===")
print("File exists:", os.path.exists("needs_review.csv"))

# 2. Simulate User clicking "Process OCR" in the dashboard
# Dashboard uses: write_to_csv=False
print("\n[Dashboard] Running wos_pipeline.run_ocr(write_to_csv=False)...")
pending = wos_pipeline.run_ocr(write_to_csv=False)
if pending:
    with open("pending_ocr.json", "w") as f:
        json.dump(pending, f)
        
print("Pending OCR entries:")
for p in pending:
    print(f"  Level {p['Level']} | Flag: {p['Flag']}")

print("\n=== Needs Review AFTER run_ocr but BEFORE approval ===")
print("File exists:", os.path.exists("needs_review.csv"))

# 3. Simulate User clicking "✅ Approve & Publish to AI Model" on the interactive table
print("\n[Dashboard] User approves data in interactive table...")
with open("pending_ocr.json", "r") as f:
    edited_df = json.load(f)

# (Dashboard logic copy-pasted)
with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"])
    for row in edited_df:
        writer.writerow({
            "File": row.get("File", "Unknown"),
            "Name": "Anonymous",
            "Level": int(row["Level"]),
            "Percent": float(row["Percent"]),
            "Damage": int(row["Damage"]),
            "Confidence": row.get("Confidence", "")
        })

print("\n=== Needs Review AFTER Approval ===")
print("File exists:", os.path.exists("needs_review.csv"))
if os.path.exists("needs_review.csv"):
    print(pd.read_csv("needs_review.csv"))

# Cleanup
if os.path.exists("images/fake_franco.png"):
    os.remove("images/fake_franco.png")
if os.path.exists("pending_ocr.json"):
    os.remove("pending_ocr.json")
