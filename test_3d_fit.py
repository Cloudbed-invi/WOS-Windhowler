import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])

def damage_model(X, A, B):
    # X is a tuple of (Level, Percent)
    L, P = X
    P_frac = P / 100.0
    start = A * np.power(L, B)
    next_start = A * np.power(L + 1.0, B)
    return start + P_frac * (next_start - start)

# Filter out Level 1 for log stability if needed, but not necessary for direct fit
df_fit = df[df['Level'] > 1]
L_data = df_fit['Level'].values
P_data = df_fit['Percent'].values
D_data = df_fit['Damage'].values

popt, _ = curve_fit(damage_model, (L_data, P_data), D_data, maxfev=10000, p0=[800, 4.0])
print(f"Global Fit: A = {popt[0]}, B = {popt[1]}")

# Let's predict Level 63 at 68% using the new fit
pred = damage_model((63, 68), popt[0], popt[1])
print(f"Predicted Lv63 @ 68%: {pred:,.0f}")
