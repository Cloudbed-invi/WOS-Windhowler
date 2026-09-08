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
import ruptures as rpt
import time

def setup_folders():
    if not os.path.exists("images"):
        os.makedirs("images")
    if not os.path.exists("needs_review.csv"):
        with open("needs_review.csv", "w", encoding="utf-8") as f:
            f.write("File,Level,Percent,Damage,Confidence,Flag_Reason\n")

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
    
    # PHASE 1.5: Otsu's Binary Thresholding (Pure Black & White)
    # This removes all background noise and makes text perfectly crisp for EasyOCR
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    optimized_path = img_path + "_opt.jpg"
    cv2.imwrite(optimized_path, thresh)
    return optimized_path

def load_formulas():
    import json, os
    try:
        with open("formulas.json", "r") as f:
            return json.load(f)
    except:
        return {"A": 591.44, "B": 4.18, "TIER_FORMULAS": []}

def get_expected_damage(level):
    import numpy as np
    config = load_formulas()
    tol_conf = config.get("TOLERANCE_CONFIRMED", 0.15)
    tol_prov = config.get("TOLERANCE_PROVISIONAL", 0.22)
    
    for tier in config.get("TIER_FORMULAS", []):
        if tier["range"][0] <= level <= tier["range"][1]:
            c = tier["coeffs"]
            expected = c[0]*(level**3) + c[1]*(level**2) + c[2]*level + c[3]
            if tier.get("provisional", True):
                return expected, "PROVISIONAL", tol_prov
            else:
                return expected, "CONFIRMED", tol_conf
            
    A = config.get("A", 591.44)
    B = config.get("B", 4.18)
    expected = A * np.power(level, B)
    return expected, "EXTRAPOLATED", 0.0 # 0 tolerance triggers unconditional review

def run_ocr(progress_callback=None):
    try:
        import easyocr
    except ImportError:
        return []
        
    reader = easyocr.Reader(['en'], gpu=True)
    
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
        
        

        try:
            damage_str = damage_match.group(1) if damage_match else None
            damage = int(damage_str.replace(',', '')) if damage_str else None
            percent_str = percent_match.group(1) if percent_match else None
            percent = int(percent_str) if percent_str else None
            level_str = level_match.group(1) if level_match else None
            level = int(level_str) if level_str else None
            
            
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
                
                # Check expected damage using tier-aware formulas
                expected_start, t_status, tol = get_expected_damage(level)
                expected_next, _, _ = get_expected_damage(level + 1)
                expected = expected_start + (percent / 100.0) * (expected_next - expected_start)
                
                if expected > 0:
                    error = abs(damage - expected) / expected
                    
                    if t_status == "EXTRAPOLATED":
                        flags.append(f"No tier fit for level {level} - manual review required")
                    elif error > tol:
                        tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                        flags.append(f"{tier_name} tier: {error*100:.1f}% deviation exceeds {int(tol*100)}% threshold")
                
                flag_reason = " | ".join(flags) if flags else ""
                
                entry = {
                    "File": filename,
                    "Level": level, 
                    "Percent": percent, 
                    "Damage": damage, 
                    "Confidence": round(avg_conf, 3),
                    "Flag": flag_reason
                }
                
                # If automated CLI is running, separate them. If dashboard, dashboard handles it.
                if flag_reason:
                    with open("needs_review.csv", mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=["File","Level","Percent","Damage","Confidence","Flag_Reason"])
                        writer.writerow({
                            "File": filename, "Level": level, "Percent": percent, 
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

def calc_loocv(L_seg, y_seg):
    n = len(L_seg)
    if n < 5: return float('inf'), float('inf')
    errors = []
    for i in range(n):
        L_train = np.delete(L_seg, i)
        y_train = np.delete(y_seg, i)
        L_test = L_seg[i]
        y_test = y_seg[i]
        weights = 1.0 / y_train
        coeffs = np.polyfit(L_train, y_train, 3, w=weights)
        pred = np.poly1d(coeffs)(L_test)
        errors.append(abs(pred - y_test) / y_test)
    return float(np.max(errors)), float(np.mean(errors))

def fit_cubic_weighted(L, y):
    if len(L) < 4: return None, float('inf'), float('inf'), float('inf')
    weights = 1.0 / y
    coeffs = np.polyfit(L, y, 3, w=weights)
    p = np.poly1d(coeffs)
    preds = p(L)
    rel_errors = np.abs(preds - y) / y
    sse_rel = np.sum(rel_errors**2)
    n = len(L)
    bic = n * np.log(max(sse_rel, 1e-15) / n) + 4 * np.log(n)
    return coeffs.tolist(), float(np.sum(rel_errors)), float(np.max(rel_errors)), float(bic)

def find_best_split(L, y, min_pts=12):
    best_bnd = None
    best_bic = float('inf')
    best_models = None
    n = len(L)
    if n < min_pts * 2: return None, best_bic, best_models
    for i in range(min_pts, n - min_pts + 1):
        bnd = L[i-1]
        L1, y1 = L[:i], y[:i]
        L2, y2 = L[i:], y[i:]
        c1, tot1, max1, bic1 = fit_cubic_weighted(L1, y1)
        c2, tot2, max2, bic2 = fit_cubic_weighted(L2, y2)
        if c1 is None or c2 is None: continue
        split_bic = bic1 + bic2
        if split_bic < best_bic:
            best_bic = split_bic
            best_bnd = int(bnd)
            best_models = (c1, c2, max1, max2)
    return best_bnd, best_bic, best_models

def find_tier_boundaries_recursive(L, y, min_pts=12):
    c_base, _, _, bic_base = fit_cubic_weighted(L, y)
    bnd, bic_split, models = find_best_split(L, y, min_pts)
    if bnd is None: return []
    # Accept if BIC is lower (penalizes the extra 4 parameters)
    if bic_split < bic_base:
        idx = np.searchsorted(L, bnd, side='right')
        left_bounds = find_tier_boundaries_recursive(L[:idx], y[:idx], min_pts)
        right_bounds = find_tier_boundaries_recursive(L[idx:], y[idx:], min_pts)
        return left_bounds + [bnd] + right_bounds
    return []

def cross_check_pelt(L, y, min_pts=12):
    try:
        log_y = np.log(y)
        algo = rpt.Pelt(model="l2", min_size=min_pts).fit(log_y)
        result = algo.predict(pen=np.log(len(y)) * log_y.var())
        return [L[i-1] for i in result if i < len(L)]
    except:
        return []


def run_ml_and_export():
    if not os.path.exists("data.csv"):
        return {}
        
    df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
    levels = df['Level'].unique()
    levels.sort()
    
    exact_formulas = {}

    
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
    
    known_levels = np.array(sorted(list(exact_formulas.keys())))
    known_starts = np.array([exact_formulas[l]["start"] for l in known_levels])
    
    # --- PHASE 1: DYNAMIC BOUNDARY DETECTION ---
    confirmed_L = []
    confirmed_EndHP = []
    for l in known_levels:
        if l == 1: continue
        confirmed_L.append(l)
        confirmed_EndHP.append(exact_formulas[l]["start"] + exact_formulas[l]["window"])
    
    # Assert distinct levels point counting logic (no raw row leakage)
    assert len(confirmed_L) == len(set(confirmed_L)), "Point count leaked raw rows!"
    
    confirmed_L = np.array(confirmed_L)
    confirmed_EndHP = np.array(confirmed_EndHP)
    
    tier_boundaries = []
    tier_formulas = []
    boundary_metadata = {}
    MIN_PTS = 12
    
    if len(confirmed_L) >= MIN_PTS:
        tier_boundaries = find_tier_boundaries_recursive(confirmed_L, confirmed_EndHP, min_pts=MIN_PTS)
        tier_boundaries.sort()
        pelt_bnds = cross_check_pelt(confirmed_L, confirmed_EndHP, min_pts=MIN_PTS)
        
        # Load history
        history = []
        if os.path.exists("boundary_history.json"):
            try:
                with open("boundary_history.json", "r") as f:
                    history = json.load(f)
            except: pass
            
        for bnd in tier_boundaries:
            # PELT Check
            pelt_agree = any(abs(pb - bnd) <= 2 for pb in pelt_bnds)
            # Stability Check
            stable = False
            if len(history) >= 2:
                r1 = history[-1]["boundaries"]
                r2 = history[-2]["boundaries"]
                if any(abs(b - bnd) <= 1 for b in r1) and any(abs(b - bnd) <= 1 for b in r2):
                    stable = True
            
            boundary_metadata[bnd] = {
                "stable": stable,
                "pelt_disagree": not pelt_agree,
                "pelt_suggestions": [int(p) for p in pelt_bnds] if not pelt_agree else []
            }
        
        # Build tier formulas
        start_idx = 0
        for bnd in tier_boundaries:
            idx = np.searchsorted(confirmed_L, bnd, side='right')
            L_seg = confirmed_L[start_idx:idx]
            y_seg = confirmed_EndHP[start_idx:idx]
            if len(L_seg) > 0:
                c, tot, max_err, _ = fit_cubic_weighted(L_seg, y_seg)
                loocv_max, loocv_mean = calc_loocv(L_seg, y_seg)
                prov = len(L_seg) < MIN_PTS or loocv_max > 0.03 # 3% LOOCV threshold
                tier_formulas.append({
                    "range": [int(L_seg[0]), int(L_seg[-1])],
                    "coeffs": c if c else [],
                    "max_error_pct": round(max_err * 100, 2) if c else 0.0,
                    "loocv_max_pct": round(loocv_max * 100, 2) if loocv_max != float('inf') else 999.0,
                    "n_points": len(L_seg),
                    "provisional": prov
                })
            start_idx = idx
            
        # Final segment
        L_seg = confirmed_L[start_idx:]
        y_seg = confirmed_EndHP[start_idx:]
        if len(L_seg) > 0:
            c, tot, max_err, _ = fit_cubic_weighted(L_seg, y_seg)
            loocv_max, loocv_mean = calc_loocv(L_seg, y_seg)
            prov = len(L_seg) < MIN_PTS or loocv_max > 0.03
            tier_formulas.append({
                "range": [int(L_seg[0]), int(L_seg[-1])],
                "coeffs": c if c else [],
                "max_error_pct": round(max_err * 100, 2) if c else 0.0,
                "loocv_max_pct": round(loocv_max * 100, 2) if loocv_max != float('inf') else 999.0,
                "n_points": len(L_seg),
                "provisional": prov
            })
            
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "n_points": len(confirmed_L),
            "boundaries": tier_boundaries
        }
        history.append(history_entry)
        with open("boundary_history.json", "w") as f:
            json.dump(history, f, indent=2)
    else:
        # Not enough data for even one segment dynamically, fallback to 1 provisional tier
        c, tot, max_err, _ = fit_cubic_weighted(confirmed_L, confirmed_EndHP)
        loocv_max, loocv_mean = calc_loocv(confirmed_L, confirmed_EndHP)
        tier_formulas.append({
            "range": [int(confirmed_L[0]) if len(confirmed_L)>0 else 1, int(confirmed_L[-1]) if len(confirmed_L)>0 else 1],
            "coeffs": c if c else [],
            "max_error_pct": round(max_err * 100, 2) if c else 0.0,
            "loocv_max_pct": round(loocv_max * 100, 2) if loocv_max != float('inf') else 999.0,
            "n_points": len(confirmed_L),
            "provisional": True
        })
    # --- END PHASE 1 ---

    max_known_confirmed = known_levels[-1]
    
    interp = PchipInterpolator(known_levels, known_starts)
    min_known_confirmed = min(known_levels) if len(known_levels) > 0 else 1
    
    all_levels = {}
    for lvl in range(1, max_known_confirmed + 1):
        if lvl in exact_formulas:
            all_levels[lvl] = exact_formulas[lvl]
        elif lvl < min_known_confirmed:
            # Rescale the extrapolated power law to anchor exactly to the lowest known confirmed level
            anchor_level = min_known_confirmed
            anchor_value = exact_formulas[anchor_level]["start"]
            scale = anchor_value / power_law(anchor_level, extrapolate_A, extrapolate_B)
            
            start = power_law(lvl, extrapolate_A, extrapolate_B) * scale
            next_start = power_law(lvl + 1, extrapolate_A, extrapolate_B) * scale
            
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start) - round(start),
                "confirmed": False,
                "extrapolated": True
            }
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
    raw_data = df[['Level', 'Percent', 'Damage']].to_dict(orient='records')
    

        
    
    adjacent_mismatches = []
    mismatch_threshold = 3.0 # tunable threshold for boundary_mismatch flagging
    
    for i in range(len(known_levels) - 1):
        lvl = known_levels[i]
        next_lvl = known_levels[i+1]
        
        if next_lvl == lvl + 1:
            start_N = exact_formulas[lvl]["start"]
            window_N = exact_formulas[lvl]["window"]
            end_N = start_N + window_N
            start_N1 = exact_formulas[next_lvl]["start"]
            
            if start_N1 > 0:
                mismatch_pct = abs(end_N - start_N1) / start_N1 * 100.0
                
                adjacent_mismatches.append({
                    "Level Pair": f"{lvl} -> {next_lvl}",
                    "End N": end_N,
                    "Start N+1": start_N1,
                    "Mismatch %": round(mismatch_pct, 3),
                    "Flagged": mismatch_pct > mismatch_threshold
                })
                
    adjacent_mismatches.sort(key=lambda x: x["Mismatch %"], reverse=True)


    js_content = f"const LAST_UPDATED = '{last_updated}';\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\n"
    js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\n"
    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\n"
    js_content += f"const ADJACENT_MISMATCHES = {json.dumps(adjacent_mismatches)};\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\n"
    
    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    formulas_config = {
        "ADJACENT_MISMATCHES": adjacent_mismatches,
        "MISMATCH_THRESHOLD": mismatch_threshold,
        "TOLERANCE_CONFIRMED": 0.15,
        "TOLERANCE_PROVISIONAL": 0.22,
        "A": extrapolate_A,
        "B": extrapolate_B,
        "TIER_BOUNDARIES": tier_boundaries,
        "BOUNDARY_METADATA": boundary_metadata,
        "TIER_FORMULAS": tier_formulas
    }
    with open("formulas.json", "w", encoding="utf-8") as f:
        json.dump(formulas_config, f, indent=2)
        
    return {
        "levels": all_levels,
        "A": extrapolate_A,
        "B": extrapolate_B
    }

if __name__ == "__main__":
    setup_folders()
    run_ml_and_export()
