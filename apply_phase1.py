import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add ruptures import at the top
if "import ruptures as rpt" not in code:
    code = code.replace("import cv2", "import cv2\nimport ruptures as rpt\nimport time")

# 2. Add Phase 1 Tier Boundary Functions before run_ml_and_export
phase1_funcs = """def fit_cubic_weighted(L, y):
    if len(L) < 4: return None, float('inf'), float('inf')
    weights = 1.0 / y
    coeffs = np.polyfit(L, y, 3, w=weights)
    p = np.poly1d(coeffs)
    preds = p(L)
    rel_errors = np.abs(preds - y) / y
    return coeffs.tolist(), float(np.sum(rel_errors)), float(np.max(rel_errors))

def find_best_split(L, y, min_pts=6):
    best_bnd, best_tot_err, best_max_err, best_models = None, float('inf'), float('inf'), None
    n = len(L)
    if n < min_pts * 2: return None, best_tot_err, best_max_err, best_models
    for i in range(min_pts, n - min_pts + 1):
        bnd = L[i-1]
        L1, y1 = L[:i], y[:i]
        L2, y2 = L[i-1:], y[i-1:] # include boundary in both for continuity! wait, prompt says split into two segments. 
        # Standard split:
        L1, y1 = L[:i], y[:i]
        L2, y2 = L[i:], y[i:]
        c1, tot1, max1 = fit_cubic_weighted(L1, y1)
        c2, tot2, max2 = fit_cubic_weighted(L2, y2)
        if c1 is None or c2 is None: continue
        tot_err = tot1 + tot2
        if tot_err < best_tot_err:
            best_tot_err = tot_err
            best_max_err = max(max1, max2)
            best_bnd = int(bnd)
            best_models = (c1, c2, tot1, tot2, max1, max2)
    return best_bnd, best_tot_err, best_max_err, best_models

def find_tier_boundaries_recursive(L, y, min_pts=6, improvement_thresh=0.10):
    c_base, tot_base, max_base = fit_cubic_weighted(L, y)
    bnd, tot_split, max_split, models = find_best_split(L, y, min_pts)
    if bnd is None: return []
    if tot_split < tot_base * (1.0 - improvement_thresh):
        idx = np.searchsorted(L, bnd, side='right')
        left_bounds = find_tier_boundaries_recursive(L[:idx], y[:idx], min_pts, improvement_thresh)
        right_bounds = find_tier_boundaries_recursive(L[idx:], y[idx:], min_pts, improvement_thresh)
        return left_bounds + [bnd] + right_bounds
    return []

"""

if "def fit_cubic_weighted" not in code:
    code = code.replace("def run_ml_and_export():", phase1_funcs + "\ndef run_ml_and_export():")

# 3. Add dynamic boundary detection inside run_ml_and_export
old_export = """    known_levels = np.array(sorted(list(exact_formulas.keys())))
    known_starts = np.array([exact_formulas[l]["start"] for l in known_levels])"""

new_export = """    known_levels = np.array(sorted(list(exact_formulas.keys())))
    known_starts = np.array([exact_formulas[l]["start"] for l in known_levels])
    
    # --- PHASE 1: DYNAMIC BOUNDARY DETECTION ---
    confirmed_L = []
    confirmed_EndHP = []
    for l in known_levels:
        if l == 1: continue
        confirmed_L.append(l)
        confirmed_EndHP.append(exact_formulas[l]["start"] + exact_formulas[l]["window"])
    
    confirmed_L = np.array(confirmed_L)
    confirmed_EndHP = np.array(confirmed_EndHP)
    
    tier_boundaries = []
    tier_formulas = []
    if len(confirmed_L) >= 6:
        tier_boundaries = find_tier_boundaries_recursive(confirmed_L, confirmed_EndHP, min_pts=6)
        tier_boundaries.sort()
        
        # Build tier formulas
        start_idx = 0
        for bnd in tier_boundaries:
            idx = np.searchsorted(confirmed_L, bnd, side='right')
            L_seg = confirmed_L[start_idx:idx]
            y_seg = confirmed_EndHP[start_idx:idx]
            if len(L_seg) >= 4:
                c, tot, max_err = fit_cubic_weighted(L_seg, y_seg)
                tier_formulas.append({
                    "range": [int(L_seg[0]), int(L_seg[-1])],
                    "coeffs": c,
                    "max_error_pct": round(max_err * 100, 2),
                    "n_points": len(L_seg)
                })
            start_idx = idx
            
        # Final segment
        L_seg = confirmed_L[start_idx:]
        y_seg = confirmed_EndHP[start_idx:]
        if len(L_seg) >= 4:
            c, tot, max_err = fit_cubic_weighted(L_seg, y_seg)
            tier_formulas.append({
                "range": [int(L_seg[0]), int(L_seg[-1])],
                "coeffs": c,
                "max_error_pct": round(max_err * 100, 2),
                "n_points": len(L_seg)
            })
            
        # Log to boundary_history.json
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "n_points": len(confirmed_L),
            "boundaries": tier_boundaries
        }
        history = []
        if os.path.exists("boundary_history.json"):
            try:
                with open("boundary_history.json", "r") as f:
                    history = json.load(f)
            except: pass
        history.append(history_entry)
        with open("boundary_history.json", "w") as f:
            json.dump(history, f, indent=2)
    # --- END PHASE 1 ---
"""

if "PHASE 1: DYNAMIC BOUNDARY DETECTION" not in code:
    code = code.replace(old_export, new_export)

# 4. Export the new tier data to exact_levels.js
old_js = """    js_content = f"const LAST_UPDATED = '{last_updated}';\\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\\n" """

new_js = """    js_content = f"const LAST_UPDATED = '{last_updated}';\\n"
    js_content += f"const EXTRAPOLATE_A = {extrapolate_A};\\n"
    js_content += f"const EXTRAPOLATE_B = {extrapolate_B};\\n"
    js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"
    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\\n" """

if "TIER_BOUNDARIES" not in code:
    code = code.replace(old_js, new_js)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
