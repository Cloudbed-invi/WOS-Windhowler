import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import HuberRegressor
import json

df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
levels = df['Level'].unique()
levels.sort()

exact_formulas = {}
for lvl in levels:
    level_data = df[df['Level'] == lvl]
    if len(level_data["Percent"].unique()) < 2:
        continue
    X = (level_data['Percent'] / 100.0).values.reshape(-1, 1)
    y = level_data['Damage'].values / 1_000_000.0
    model = HuberRegressor(epsilon=1.35)
    model.fit(X, y)
    exact_formulas[int(lvl)] = {
        "start": model.intercept_ * 1_000_000,
        "window": model.coef_[0] * 1_000_000
    }

known_L = np.array(sorted(list(exact_formulas.keys())))
known_S = np.array([exact_formulas[l]["start"] for l in known_L])

def power_law(x, a, b):
    return a * np.power(x, b)

def exp_law(x, a, b):
    return a * np.exp(b * x)

# Ignore level 1 because start is 0, ruins log fits
fit_L = known_L[known_L > 1]
fit_S = known_S[known_L > 1]

popt_pow, _ = curve_fit(power_law, fit_L, fit_S, maxfev=10000)
popt_exp, _ = curve_fit(exp_law, fit_L, fit_S, maxfev=10000)

print(f"Power Law: {popt_pow[0]:.2f} * L^{popt_pow[1]:.4f}")
print(f"Exp Law: {popt_exp[0]:.2f} * e^({popt_exp[1]:.4f} * L)")

# Predict 49 and compare
print("Real 49:", exact_formulas.get(49, {}).get("start"))
print("Power 49:", power_law(49, *popt_pow))
print("Exp 49:", exp_law(49, *popt_exp))

# Predict 56 and compare (Real damage was ~11.9B at 2%)
print("Power 56:", power_law(56, *popt_pow))
print("Exp 56:", exp_law(56, *popt_exp))
