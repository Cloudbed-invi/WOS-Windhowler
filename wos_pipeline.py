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
    if not os.path.exists("needs_review.csv"):
        with open("needs_review.csv", "w", encoding="utf-8") as f:
            f.write("File,Name,Level,Percent,Damage,Confidence,Flag_Reason\n")

def optimize_image_for_ocr(img_path):
    img = cv2.imread(img_path)
    if img is None: return img_path
    
    # PHASE 1: Upscale 2x using cubic interpolation
    width = int(img.shape[1] * 2)
    height = int(img.shape[0] * 2)
    img_up = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    
    # PHASE 1: Convert to Grayscale
    gray = cv2.cvtColor(img_up, cv2.COLOR_BGR2GRAY)
    
    # PHASE 1: CLAHE Contrast Enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    optimized_path = img_path + "_opt.jpg"
    cv2.imwrite(optimized_path, enhanced)
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
        opt_path = optimize_image_for_ocr(img_path)
        
        # detail=1 returns (bbox, text, probability)
        results = reader.readtext(opt_path, detail=1)
        full_text = " ".join([res[1] for res in results])
        
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
            damage_str = damage_match.group(1) if damage_match else None
            damage = int(damage_str.replace(',', '')) if damage_str else None
            percent_str = percent_match.group(1) if percent_match else None
            percent = int(percent_str) if percent_str else None
            level_str = level_match.group(1) if level_match else None
            level = int(level_str) if level_str else None
            name = name.replace('J', ']') if '[' in name and 'J' in name else name
            
            # Calculate targeted OCR Confidence
            confidences = []
            for bbox, text, prob in results:
                if (damage_str and damage_str in text) or \
                   (percent_str and percent_str in text) or \
                   (level_str and level_str in text):
                    confidences.append(prob)
            
            avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
            
            if damage and level and percent is not None:
                # Sanity Checks
                flags = []
                if avg_conf < 0.70:
                    flags.append(f"Low OCR Confidence ({avg_conf:.2f})")
                
                # Check expected damage boundary (Monotonic/Curve Deviation Check)
                expected = 602.34 * np.power(level, 4.1763)
                if expected > 0:
                    error = abs(damage - expected) / expected
                    if error > 0.50:  # If it deviates wildly (50%+) from the baseline power curve
                        flags.append(f"Curve Deviation > 50% (Expected ~{int(expected)})")
                
                flag_reason = " | ".join(flags) if flags else ""
                
                entry = {
                    "File": filename,
                    "Name": name, 
                    "Level": level, 
                    "Percent": percent, 
                    "Damage": damage, 
                    "Confidence": round(avg_conf, 3),
                    "Flag": flag_reason
                }
                
                # If automated CLI is running, separate them. If dashboard, dashboard handles it.
                if flag_reason:
                    with open("needs_review.csv", mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=["File","Name","Level","Percent","Damage","Confidence","Flag_Reason"])
                        writer.writerow({
                            "File": filename, "Name": name, "Level": level, "Percent": percent, 
                            "Damage": damage, "Confidence": round(avg_conf, 3), "Flag_Reason": flag_reason
                        })
                
                new_entries.append(entry)
        except Exception as e:
            pass
            
        if opt_path != img_path and os.path.exists(opt_path):
            os.remove(opt_path)
        
        if progress_callback:
            progress_callback(i + 1, total)
            
    return new_entries

# Keep remainder of ML pipeline intact for this phase...
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
