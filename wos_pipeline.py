import os
import re
import csv
import json
import pandas as pd
from sklearn.linear_model import HuberRegressor

def setup_folders():
    if not os.path.exists("images"):
        os.makedirs("images")

def run_ocr(progress_callback=None):
    try:
        import easyocr
    except ImportError:
        return False
        
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)
    csv_file = "data.csv"
    
    image_files = [f for f in os.listdir("images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total = len(image_files)
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
        writer.writeheader()
        
        for i, filename in enumerate(image_files):
            img_path = os.path.join("images", filename)
            results = reader.readtext(img_path, detail=0)
            full_text = " ".join(results)
            
            damage_match = re.search(r'dealt\s+([\d,]+)\s+damage', full_text)
            percent_match = re.search(r'reaching\s+(\d+)%', full_text)
            level_match = re.search(r'Lv[.,\s_]*(\d+)', full_text)
            name = "Unknown"
            if "Overview" in full_text and "Windhowler" in full_text:
                try:
                    name_part = full_text.split("Overview")[1].split("Windhowler")[0].strip()
                    if name_part: name = name_part
                except: pass

            try:
                damage = int(damage_match.group(1).replace(',', '')) if damage_match else None
                percent = int(percent_match.group(1)) if percent_match else None
                level = int(level_match.group(1)) if level_match else None
                name = name.replace('J', ']') if '[' in name and 'J' in name else name
                
                if damage and level:
                    writer.writerow({"Name": name, "Level": level, "Percent": percent, "Damage": damage, "File": filename})
            except Exception:
                pass
            
            if progress_callback:
                progress_callback(i + 1, total)
                
    return True

def run_ml_and_export():
    if not os.path.exists("data.csv"):
        return {}
        
    df = pd.read_csv("data.csv")
    levels = df['Level'].unique()
    levels.sort()
    
    exact_formulas = {}
    
    # Preserve Level 1 starting point logic if we have it
    if 1 not in levels:
        exact_formulas[1] = {"start": 0, "window": 24300}
        
    # Preserve Level 25 from earlier data
    if 25 not in levels:
        exact_formulas[25] = {"start": 386739898, "window": 71536909}
    
    for lvl in levels:
        level_data = df[df['Level'] == lvl]
        if len(level_data) < 2:
            continue
            
        X = (level_data['Percent'] / 100.0).values.reshape(-1, 1)
        y = level_data['Damage'].values
        y_scaled = y / 1_000_000.0
        
        model = HuberRegressor(epsilon=1.35)
        model.fit(X, y_scaled)
        
        window_size = model.coef_[0] * 1_000_000
        start_damage = model.intercept_ * 1_000_000
        
        exact_formulas[int(lvl)] = {
            "start": round(start_damage),
            "window": round(window_size)
        }
        
    # Automate saving directly to the exact_levels.js file
    js_content = "const EXACT_LEVELS = " + json.dumps(exact_formulas, indent=2) + ";"
    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return exact_formulas

if __name__ == "__main__":
    setup_folders()
    if run_ocr():
        run_ml_and_export()
        print("Updated exact_levels.js automatically!")
