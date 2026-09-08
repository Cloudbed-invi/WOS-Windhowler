import re
import json

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove fake level 1 anchor
old_lvl_1 = """    if 1 not in levels:
        exact_formulas[1] = {"start": 0, "window": 24300, "confirmed": True}"""
code = code.replace(old_lvl_1, "")

# 2. Fix interpolation loop
old_loop = """    interp = PchipInterpolator(known_levels, known_starts)
    
    all_levels = {}
    for lvl in range(1, max_known_confirmed + 1):
        if lvl in exact_formulas:
            all_levels[lvl] = exact_formulas[lvl]
        else:
            start = float(interp(lvl))
            next_start = float(interp(lvl + 1))
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False
            }"""

new_loop = """    interp = PchipInterpolator(known_levels, known_starts)
    min_known_confirmed = min(known_levels) if known_levels else 1
    
    all_levels = {}
    for lvl in range(1, max_known_confirmed + 1):
        if lvl in exact_formulas:
            all_levels[lvl] = exact_formulas[lvl]
        elif lvl < min_known_confirmed:
            start = power_law(lvl, extrapolate_A, extrapolate_B)
            next_start = power_law(lvl + 1, extrapolate_A, extrapolate_B)
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False,
                "extrapolated": True
            }
        else:
            start = float(interp(lvl))
            next_start = float(interp(lvl + 1))
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False
            }"""
code = code.replace(old_loop, new_loop)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)

