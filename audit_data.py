import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

df = pd.read_csv("data.csv")

def global_damage_model(X, A, B):
    L, P = X
    P_frac = P / 100.0
    start = A * np.power(L, B)
    next_start = A * np.power(L + 1.0, B)
    return start + P_frac * (next_start - start)

# Fit the curve using only "sane" looking data to get a baseline
# (Since we might have anomalies, let's just use a known good approximation)
A = 602.34
B = 4.1763

anomalies = []
for idx, row in df.iterrows():
    lvl = float(row['Level'])
    pct = float(row['Percent'])
    dmg = float(row['Damage'])
    
    expected = global_damage_model((lvl, pct), A, B)
    error = abs(dmg - expected) / expected
    
    if error > 0.15: # 15% deviation
        anomalies.append({
            "Level": lvl, "Percent": pct, "Damage": dmg, "Error": f"{error*100:.1f}%", "File": row['File']
        })

print(f"Found {len(anomalies)} severe anomalies out of {len(df)} rows:")
for a in anomalies:
    print(a)
