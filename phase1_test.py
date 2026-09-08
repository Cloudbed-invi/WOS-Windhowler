import json
import numpy as np
import pandas as pd
import ruptures as rpt
from sklearn.linear_model import HuberRegressor

def get_confirmed_data():
    df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
    levels = df['Level'].unique()
    levels.sort()
    L = []
    End_HP = []
    
    for lvl in levels:
        if lvl == 1: continue
        level_data = df[df['Level'] == lvl]
        if len(level_data["Percent"].unique()) < 2: continue
        X = (level_data['Percent'] / 100.0).values.reshape(-1, 1)
        y = level_data['Damage'].values
        model = HuberRegressor(epsilon=1.35)
        model.fit(X, y / 1_000_000.0)
        start = model.intercept_ * 1_000_000
        window = model.coef_[0] * 1_000_000
        L.append(int(lvl))
        End_HP.append(start + window)
    
    return np.array(L), np.array(End_HP)

def fit_cubic_weighted(L, y):
    if len(L) < 4:
        return None, float('inf'), float('inf')
    weights = 1.0 / y
    coeffs = np.polyfit(L, y, 3, w=weights)
    p = np.poly1d(coeffs)
    preds = p(L)
    rel_errors = np.abs(preds - y) / y
    return coeffs, np.sum(rel_errors), np.max(rel_errors)

def find_best_split(L, y, min_pts=6):
    best_bnd = None
    best_tot_err = float('inf')
    best_max_err = float('inf')
    best_models = None
    
    n = len(L)
    if n < min_pts * 2:
        return None, best_tot_err, best_max_err, best_models
        
    for i in range(min_pts, n - min_pts):
        bnd = L[i-1]
        
        L1, y1 = L[:i], y[:i]
        L2, y2 = L[i:], y[i:]
        
        c1, tot1, max1 = fit_cubic_weighted(L1, y1)
        c2, tot2, max2 = fit_cubic_weighted(L2, y2)
        
        if c1 is None or c2 is None: continue
        
        tot_err = tot1 + tot2
        max_err = max(max1, max2)
        
        if tot_err < best_tot_err:
            best_tot_err = tot_err
            best_max_err = max_err
            best_bnd = bnd
            best_models = (c1, c2, tot1, tot2, max1, max2)
            
    return best_bnd, best_tot_err, best_max_err, best_models

def find_tier_boundaries_recursive(L, y, min_pts=6, improvement_thresh=0.10):
    c_base, tot_base, max_base = fit_cubic_weighted(L, y)
    bnd, tot_split, max_split, models = find_best_split(L, y, min_pts)
    
    if bnd is None:
        return []
        
    if tot_split < tot_base * (1.0 - improvement_thresh):
        idx = np.searchsorted(L, bnd, side='right')
        L1, y1 = L[:idx], y[:idx]
        L2, y2 = L[idx:], y[idx:]
        
        left_bounds = find_tier_boundaries_recursive(L1, y1, min_pts, improvement_thresh)
        right_bounds = find_tier_boundaries_recursive(L2, y2, min_pts, improvement_thresh)
        
        return left_bounds + [int(bnd)] + right_bounds
    else:
        return []

def cross_check_pelt(y, L):
    log_y = np.log(y)
    algo = rpt.Pelt(model="l2", min_size=5).fit(log_y)
    result = algo.predict(pen=np.log(len(y)) * log_y.var())
    return [L[i-1] for i in result if i < len(L)]

if __name__ == "__main__":
    L, y = get_confirmed_data()
    print("Running Baseline Cubic on ALL confirmed levels:")
    base_c, base_tot, base_max = fit_cubic_weighted(L, y)
    print(f"Base Max Error: {base_max*100:.2f}% | Mean Error: {(base_tot/len(L))*100:.2f}%")
    
    print("\nRunning Dynamic Recursive Boundary Search...")
    boundaries = find_tier_boundaries_recursive(L, y, min_pts=6)
    print(f"Found boundaries: {boundaries}")
    
    bnd_to_check = 27
    print(f"\nChecking Level {bnd_to_check} manually to compare with dynamic boundaries...")
    idx = np.searchsorted(L, bnd_to_check, side='right')
    L1, y1 = L[:idx], y[:idx]
    L2, y2 = L[idx:], y[idx:]
    c1, _, max1 = fit_cubic_weighted(L1, y1)
    c2, _, max2 = fit_cubic_weighted(L2, y2)
    
    p1 = np.poly1d(c1)
    p2 = np.poly1d(c2)
    val1 = p1(bnd_to_check)
    val2 = p2(bnd_to_check)
    mismatch = abs(val1 - val2) / ((val1 + val2)/2.0)
    print(f"Continuity at Level {bnd_to_check}: {mismatch*100:.3f}% mismatch")
    print(f"Tier 1 Max Error: {max1*100:.2f}%")
    print(f"Tier 2 Max Error: {max2*100:.2f}%")
    
    print("\nPELT Cross-Check (ruptures):")
    try:
        pelt_bnds = cross_check_pelt(y, L)
        print(f"PELT proposes boundaries at: {pelt_bnds}")
    except Exception as e:
        print(f"PELT Error: {e}")
