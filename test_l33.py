import pandas as pd
import numpy as np
import wos_pipeline
from sklearn.linear_model import HuberRegressor

df = pd.read_csv("data.csv")

# Get existing Level 33 data
l33 = df[df["Level"] == 33]
print("--- Old Fit ---")
X_old = l33["Percent"].values.reshape(-1, 1) / 100.0
y_old = l33["Damage"].values
huber_old = HuberRegressor(epsilon=1.35).fit(X_old, y_old / 1_000_000.0)
start_old = huber_old.intercept_ * 1_000_000.0
window_old = huber_old.coef_[0] * 1_000_000.0
print(f"Start: {start_old:,.0f} | Window: {window_old:,.0f}")
print(f"Prediction for 60%: {(start_old + 0.60 * window_old):,.0f} (vs 1,487,367,636)")

# Add new point
new_row = {"File": "media_1788925556344.png", "Name": "Community", "Level": 33, "Percent": 60.0, "Damage": 1487367636, "Confidence": 1.0}
df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

l33_new = df_new[df_new["Level"] == 33]
print("\n--- New Fit (with 60% point) ---")
X_new = l33_new["Percent"].values.reshape(-1, 1) / 100.0
y_new = l33_new["Damage"].values
huber_new = HuberRegressor(epsilon=1.35).fit(X_new, y_new / 1_000_000.0)
start_new = huber_new.intercept_ * 1_000_000.0
window_new = huber_new.coef_[0] * 1_000_000.0
print(f"Start: {start_new:,.0f} | Window: {window_new:,.0f}")
print(f"Prediction for 60%: {(start_new + 0.60 * window_new):,.0f}")
print(f"Prediction for 8%: {(start_new + 0.08 * window_new):,.0f} (vs ~1,390,500,000)")
print(f"Prediction for 15%: {(start_new + 0.15 * window_new):,.0f} (vs 1,404,307,520)")

shift = abs(window_new - window_old) / window_old
print(f"\nWindow Shift: {shift*100:.2f}%")

