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
import cv2

def setup_folders():
    if not os.path.exists("images"):
        os.makedirs("images")

def optimize_image_for_ocr(img_path):
    # Read with OpenCV, convert to Grayscale, and apply Contrast/Thresholding
    img = cv2.imread(img_path)
    if img is None: return img_path
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Increase contrast
    alpha = 1.5
    beta = 0
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
    optimized_path = img_path + "_opt.jpg"
    cv2.imwrite(optimized_path, adjusted)
    return optimized_path

def run_ocr(progress_callback=None):
    try:
        import easyocr
    except ImportError:
        return []
        
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)
    
    image_files = [f for f in os.listdir("images") if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.endswith('_opt.jpg')]
    total = len(image_files)
    if total == 0: return []
    
    new_entries = []
    for i, filename in enumerate(image_files):
        img_path = os.path.join("images", filename)
            
            # OPTIMIZATION: Pre-process image with OpenCV
            opt_path = optimize_image_for_ocr(img_path)
            
            # OPTIMIZATION: Restrict allowed characters to reduce hallucinations
            results = reader.readtext(opt_path, detail=0)
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
                
                if damage and level and percent is not None:
                    entry = {"Name": name, "Level": level, "Percent": percent, "Damage": damage, "File": filename}
                    new_entries.append(entry)
            except Exception:
                pass
                
            # Cleanup optimized temp file
            if opt_path != img_path and os.path.exists(opt_path):
                os.remove(opt_path)
            
            if progress_callback:
                progress_callback(i + 1, total)
                
    return new_entries

def power_law(x, a, b):
    return a * np.power(x, b)

def global_damage_model(X, A, B):
    L, P = X
    P_frac = P / 100.0
    start = A * np.power(L, B)
    next_start = A * np.power(L + 1.0, B)
    return start + P_frac * (next_start - start)

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
    
    df_fit = df[df['Level'] > 1]
    if not df_fit.empty:
        L_data = df_fit['Level'].values
        P_data = df_fit['Percent'].values
        D_data = df_fit['Damage'].values
        try:
            popt, _ = curve_fit(global_damage_model, (L_data, P_data), D_data, maxfev=10000, p0=[800, 4.0])
            extrapolate_A = popt[0]
            extrapolate_B = popt[1]
        except:
            extrapolate_A = 844.19
            extrapolate_B = 4.0878
    else:
        extrapolate_A = 844.19
        extrapolate_B = 4.0878
    
    known_levels = np.array(sorted(list(exact_formulas.keys())))
    known_starts = np.array([exact_formulas[l]["start"] for l in known_levels])
    max_known_confirmed = known_levels[-1]
    
    interp = PchipInterpolator(known_levels, known_starts)
    
    all_levels = {}
    for lvl in range(1, max_known_confirmed + 1):
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
            
    highest_raw_level = int(df['Level'].max())
    extrapolate_target = max(60, highest_raw_level + 2)
    
    for lvl in range(max_known_confirmed + 1, extrapolate_target + 1):
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
        
    return {
        "levels": all_levels,
        "A": extrapolate_A,
        "B": extrapolate_B
    }

if __name__ == "__main__":
    setup_folders()
    run_ml_and_export()


