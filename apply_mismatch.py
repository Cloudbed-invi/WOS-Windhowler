import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add adjacent mismatch logic before formulas_config
target = "formulas_config = {"

mismatch_logic = """
    adjacent_mismatches = []
    mismatch_threshold = 3.0 # tunable threshold for boundary_mismatch flagging
    
    for i in range(len(known_levels) - 1):
        lvl = known_levels[i]
        next_lvl = known_levels[i+1]
        
        if next_lvl == lvl + 1:
            start_N = exact_formulas[lvl]["start"]
            window_N = exact_formulas[lvl]["window"]
            end_N = start_N + window_N
            start_N1 = exact_formulas[next_lvl]["start"]
            
            if start_N1 > 0:
                mismatch_pct = abs(end_N - start_N1) / start_N1 * 100.0
                
                adjacent_mismatches.append({
                    "Level Pair": f"{lvl} -> {next_lvl}",
                    "End N": end_N,
                    "Start N+1": start_N1,
                    "Mismatch %": round(mismatch_pct, 3),
                    "Flagged": mismatch_pct > mismatch_threshold
                })
                
    adjacent_mismatches.sort(key=lambda x: x["Mismatch %"], reverse=True)

"""

new_target = mismatch_logic + "\n    formulas_config = {"
code = code.replace(target, new_target)

# 2. Add to formulas_config
old_config = """    formulas_config = {
        "TOLERANCE_CONFIRMED": 0.15,
        "TOLERANCE_PROVISIONAL": 0.22,"""

new_config = """    formulas_config = {
        "ADJACENT_MISMATCHES": adjacent_mismatches,
        "MISMATCH_THRESHOLD": mismatch_threshold,
        "TOLERANCE_CONFIRMED": 0.15,
        "TOLERANCE_PROVISIONAL": 0.22,"""
code = code.replace(old_config, new_config)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
