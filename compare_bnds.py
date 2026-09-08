import numpy as np
import pandas as pd
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

def calc_loocv_errors(L_seg, y_seg):
    n = len(L_seg)
    if n < 5: return []
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
    return errors

L, y = get_confirmed_data()

for bnd in [34, 39]:
    idx = np.searchsorted(L, bnd, side='right')
    L1, y1 = L[:idx], y[:idx]
    L2, y2 = L[idx:], y[idx:]
    
    err1 = calc_loocv_errors(L1, y1)
    err2 = calc_loocv_errors(L2, y2)
    
    all_errs = err1 + err2
    
    print(f"\nBoundary {bnd}:")
    if err1:
        print(f"  Tier 1 ({len(L1)} pts): Max LOOCV = {np.max(err1)*100:.2f}% | Mean = {np.mean(err1)*100:.2f}%")
    if err2:
        print(f"  Tier 2 ({len(L2)} pts): Max LOOCV = {np.max(err2)*100:.2f}% | Mean = {np.mean(err2)*100:.2f}%")
    if all_errs:
        print(f"  COMBINED OVERALL:")
        print(f"    Max LOOCV Error:  {np.max(all_errs)*100:.2f}%")
        print(f"    Mean LOOCV Error: {np.mean(all_errs)*100:.2f}%")
