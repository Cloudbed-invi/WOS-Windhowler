import re
import json

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add calc_loocv function before fit_cubic_weighted
loocv_func = """def calc_loocv(L_seg, y_seg):
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

def fit_cubic_weighted"""

code = code.replace("def fit_cubic_weighted", loocv_func)

# 2. Update loop in run_ml_and_export to calculate LOOCV and append to tier_formulas
old_loop = """        # Build tier formulas
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
            })"""

new_loop = """        # Build tier formulas
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
            })"""

code = code.replace(old_loop, new_loop)

# 3. Also fix the fallback block at the end (when len < MIN_PTS)
old_fallback = """        # Not enough data for even one segment dynamically, fallback to 1 provisional tier
        c, tot, max_err, _ = fit_cubic_weighted(confirmed_L, confirmed_EndHP)
        tier_formulas.append({
            "range": [int(confirmed_L[0]) if len(confirmed_L)>0 else 1, int(confirmed_L[-1]) if len(confirmed_L)>0 else 1],
            "coeffs": c if c else [],
            "max_error_pct": round(max_err * 100, 2) if c else 0.0,
            "n_points": len(confirmed_L),
            "provisional": True
        })"""

new_fallback = """        # Not enough data for even one segment dynamically, fallback to 1 provisional tier
        c, tot, max_err, _ = fit_cubic_weighted(confirmed_L, confirmed_EndHP)
        loocv_max, loocv_mean = calc_loocv(confirmed_L, confirmed_EndHP)
        tier_formulas.append({
            "range": [int(confirmed_L[0]) if len(confirmed_L)>0 else 1, int(confirmed_L[-1]) if len(confirmed_L)>0 else 1],
            "coeffs": c if c else [],
            "max_error_pct": round(max_err * 100, 2) if c else 0.0,
            "loocv_max_pct": round(loocv_max * 100, 2) if loocv_max != float('inf') else 999.0,
            "n_points": len(confirmed_L),
            "provisional": True
        })"""

code = code.replace(old_fallback, new_fallback)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
