import re
import json
from datetime import datetime

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the phase 1 functions block
new_funcs = """def fit_cubic_weighted(L, y):
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
"""

# Regex out old functions
code = re.sub(r'def fit_cubic_weighted.*?return \[\]\n\n', new_funcs + '\n', code, flags=re.DOTALL)

# Update run_ml_and_export
new_export = """    known_levels = np.array(sorted(list(exact_formulas.keys())))
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
                tier_formulas.append({
                    "range": [int(L_seg[0]), int(L_seg[-1])],
                    "coeffs": c if c else [],
                    "max_error_pct": round(max_err * 100, 2) if c else 0.0,
                    "n_points": len(L_seg),
                    "provisional": len(L_seg) < MIN_PTS
                })
            start_idx = idx
            
        # Final segment
        L_seg = confirmed_L[start_idx:]
        y_seg = confirmed_EndHP[start_idx:]
        if len(L_seg) > 0:
            c, tot, max_err, _ = fit_cubic_weighted(L_seg, y_seg)
            tier_formulas.append({
                "range": [int(L_seg[0]), int(L_seg[-1])],
                "coeffs": c if c else [],
                "max_error_pct": round(max_err * 100, 2) if c else 0.0,
                "n_points": len(L_seg),
                "provisional": len(L_seg) < MIN_PTS
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
        tier_formulas.append({
            "range": [int(confirmed_L[0]) if len(confirmed_L)>0 else 1, int(confirmed_L[-1]) if len(confirmed_L)>0 else 1],
            "coeffs": c if c else [],
            "max_error_pct": round(max_err * 100, 2) if c else 0.0,
            "n_points": len(confirmed_L),
            "provisional": True
        })
    # --- END PHASE 1 ---
"""

code = re.sub(r'    # --- PHASE 1: DYNAMIC BOUNDARY DETECTION ---.*?    # --- END PHASE 1 ---\n', new_export, code, flags=re.DOTALL)

# Update js export to include BOUNDARY_METADATA
new_js = """    js_content += f"const TIER_BOUNDARIES = {json.dumps(tier_boundaries)};\\n"\n    js_content += f"const BOUNDARY_METADATA = {json.dumps(boundary_metadata)};\\n"\n    js_content += "const TIER_FORMULAS = " + json.dumps(tier_formulas, indent=2) + ";\\n" """
code = re.sub(r'    js_content \+= f"const TIER_BOUNDARIES = \{json\.dumps\(tier_boundaries\)\};\\n"\n    js_content \+= "const TIER_FORMULAS = " \+ json\.dumps\(tier_formulas, indent=2\) \+ ";\\n"', new_js, code)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
