import os
import re
import csv
import json
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import HuberRegressor
from scipy.interpolate import PchipInterpolator
from scipy.optimize import curve_fit

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
    if total == 0: return True
    
    # Optional: read existing CSV to prevent double-processing files
    processed_files = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader_csv = csv.DictReader(f)
            if "File" in reader_csv.fieldnames:
                for row in reader_csv:
                    processed_files.add(row["File"])
                    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        # Write header if file is empty
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
            writer.writeheader()
        else:
            writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
            
        for i, filename in enumerate(image_files):
            if filename in processed_files:
                if progress_callback: progress_callback(i + 1, total)
                continue
                
            img_path = os.path.join("images", filename)
            results = reader.readtext(img_path, detail=0)
            full_text = " ".join(results)
            
            damage_match = re.search(r'dealt\s+([\d,]+)\s+damage', full_text, re.IGNORECASE)
            percent_match = re.search(r'reaching\s+(\d+)%', full_text, re.IGNORECASE)
            level_match = re.search(r'Lv[.,\s_]*(\d+)', full_text, re.IGNORECASE)
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

def power_law(x, a, b):
    return a * np.power(x, b)

def run_ml_and_export():
    if not os.path.exists("data.csv"):
        return {}
        
    df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
    levels = df['Level'].unique()
    levels.sort()
    
    exact_formulas = {}
    if 1 not in levels:
        exact_formulas[1] = {"start": 0, "window": 24300, "confirmed": True}
    
    for lvl in levels:
        level_data = df[df['Level'] == lvl]
        if len(level_data["Percent"].unique()) < 2:
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
            "window": round(window_size),
            "confirmed": True
        }
    
    known_levels = np.array(sorted(list(exact_formulas.keys())))
    known_starts = np.array([exact_formulas[l]["start"] for l in known_levels])
    
    fit_L = known_levels[known_levels > 1]
    fit_S = known_starts[known_levels > 1]
    popt, _ = curve_fit(power_law, fit_L, fit_S, maxfev=10000)
    extrapolate_A = popt[0]
    extrapolate_B = popt[1]
    
    max_known = known_levels[-1]
    interp = PchipInterpolator(known_levels, known_starts)
    
    all_levels = {}
    for lvl in range(1, max_known + 1):
        if lvl in exact_formulas:
            all_levels[lvl] = exact_formulas[lvl]
        else:
            start = float(interp(lvl))
            next_start = float(interp(lvl + 1))
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False
            }
            
    for lvl in range(max_known + 1, 61):
        start = power_law(lvl, extrapolate_A, extrapolate_B)
        next_start = power_law(lvl + 1, extrapolate_A, extrapolate_B)
        all_levels[lvl] = {
            "start": round(start),
            "window": round(next_start - start),
            "confirmed": False,
            "extrapolated": True
        }
        
    last_updated = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    raw_data = df[['Level', 'Percent', 'Damage', 'Name']].to_dict(orient='records')
    
    js_content = f"const LAST_UPDATED = '{last_updated}';\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\n"
    
    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return all_levels

if __name__ == "__main__":
    setup_folders()
    run_ml_and_export()
