import os
import re
import csv
import json
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import HuberRegressor
from scipy.interpolate import PchipInterpolator

def setup_folders():
    if not os.path.exists("images"):
        os.makedirs("images")

def run_ml_and_export():
    if not os.path.exists("data.csv"):
        return {}
        
    df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
    levels = df['Level'].unique()
    levels.sort()
    
    exact_formulas = {}
    if 1 not in levels:
        exact_formulas[1] = {"start": 0, "window": 24300, "confirmed": True}
    
    for lvl in levels:
        level_data = df[df['Level'] == lvl]
        if len(level_data["Percent"].unique()) < 2:
            continue
            
        X = (level_data['Percent'] / 100.0).values.reshape(-1, 1)
        y = level_data['Damage'].values
        y_scaled = y / 1_000_000.0
        
        model = HuberRegressor(epsilon=1.35)
        model.fit(X, y_scaled)
        
        window_size = model.coef_[0] * 1_000_000
        start_damage = model.intercept_ * 1_000_000
        
        exact_formulas[int(lvl)] = {
            "start": round(start_damage),
            "window": round(window_size),
            "confirmed": True
        }
    
    # Interpolate missing levels
    known_levels = sorted(list(exact_formulas.keys()))
    known_starts = [exact_formulas[l]["start"] for l in known_levels]
    
    # We must add an artificial anchor at the end so interpolation works up to level 60
    if known_levels[-1] < 60:
        known_levels.append(60)
        # extrapolate the last window roughly
        last_window = exact_formulas[known_levels[-2]]["window"]
        known_starts.append(known_starts[-1] + (last_window * 1.1 * (60 - known_levels[-2])))
        
    interp = PchipInterpolator(known_levels, known_starts)
    
    all_levels = {}
    for lvl in range(1, 51):
        if lvl in exact_formulas:
            all_levels[lvl] = exact_formulas[lvl]
        else:
            start = float(interp(lvl))
            next_start = float(interp(lvl + 1))
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False
            }
        
    last_updated = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    raw_data = df[['Level', 'Percent', 'Damage', 'Name']].to_dict(orient='records')
    
    js_content = f"const LAST_UPDATED = '{last_updated}';\n"
    js_content += "const EXACT_LEVELS = " + json.dumps(all_levels, indent=2) + ";\n"
    js_content += "const RAW_DATA = " + json.dumps(raw_data, indent=2) + ";\n"
    
    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return all_levels

if __name__ == "__main__":
    setup_folders()
    run_ml_and_export()
