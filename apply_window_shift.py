import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add check_window_shift function before run_ocr
target = "def run_ocr(progress_callback=None):"
new_func = """def check_window_shift(level, percent, damage):
    \"\"\"
    Temporarily refits the Huber regression for a confirmed level including the new point.
    Returns the percentage shift in the window coefficient.
    \"\"\"
    import pandas as pd
    import numpy as np
    import os
    from sklearn.linear_model import HuberRegressor
    
    expected_start, status, _ = get_expected_damage(level)
    if status != "CONFIRMED":
        return 0.0
        
    expected_next, _, _ = get_expected_damage(level + 1)
    old_window = expected_next - expected_start
    
    if old_window <= 0:
        return 0.0
        
    if not os.path.exists("data.csv"):
        return 0.0
        
    df = pd.read_csv("data.csv")
    level_data = df[df['Level'] == level]
    
    if len(level_data["Percent"].unique()) < 2:
        return 0.0
        
    X_new = np.append(level_data['Percent'].values, percent).reshape(-1, 1) / 100.0
    y_new = np.append(level_data['Damage'].values, damage)
    
    try:
        huber = HuberRegressor().fit(X_new, y_new)
        new_window = huber.coef_[0]
        shift = abs(new_window - old_window) / old_window
        return float(shift)
    except:
        return 0.0

"""
code = code.replace(target, new_func + target)

# 2. Update run_ocr to use it
old_ocr = """                    if t_status == "EXTRAPOLATED":
                        flags.append(f"No tier fit for level {level} - manual review required")
                    elif error > tol:
                        tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                        flags.append(f"{tier_name} tier: {error*100:.1f}% deviation exceeds {int(tol*100)}% threshold")"""

new_ocr = """                    if t_status == "EXTRAPOLATED":
                        flags.append(f"No tier fit for level {level} - manual review required")
                    elif error > tol:
                        tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                        flags.append(f"{tier_name} tier: {error*100:.1f}% deviation exceeds {int(tol*100)}% threshold")
                        
                    # Window Shift Check
                    if t_status == "CONFIRMED":
                        shift = check_window_shift(level, percent, damage)
                        if shift > 0.05:
                            flags.append(f"window shift: {shift*100:.1f}% - possible different account")"""

code = code.replace(old_ocr, new_ocr)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
