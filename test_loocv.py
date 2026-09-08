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

def calc_loocv(L_seg, y_seg):
    n = len(L_seg)
    if n < 5: return float('inf'), float('inf') # Can't LOOCV a cubic with < 5 points
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
    return np.max(errors), np.mean(errors)

L, y = get_confirmed_data()

# Evaluate 4-tier split [29, 38, 46]
boundaries = [29, 38, 46]
print("LOOCV Results for 4-tier setup (min_pts=6):")
start_idx = 0
bnds = boundaries + [L[-1]+1]
for bnd in bnds:
    idx = np.searchsorted(L, bnd, side='right')
    L_seg = L[start_idx:idx]
    y_seg = y[start_idx:idx]
    if len(L_seg) > 0:
        c = np.polyfit(L_seg, y_seg, 3, w=1.0/y_seg)
        train_max = np.max(np.abs(np.poly1d(c)(L_seg) - y_seg) / y_seg)
        loocv_max, loocv_mean = calc_loocv(L_seg, y_seg)
        print(f"Tier {L_seg[0]}-{L_seg[-1]} (n={len(L_seg)}):")
        print(f"  Training Max Error: {train_max*100:.2f}%")
        print(f"  LOOCV Max Error:    {loocv_max*100:.2f}%")
    start_idx = idx
