with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_loop = """        elif lvl < min_known_confirmed:
            start = power_law(lvl, extrapolate_A, extrapolate_B)
            next_start = power_law(lvl + 1, extrapolate_A, extrapolate_B)
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False,
                "extrapolated": True
            }"""

new_loop = """        elif lvl < min_known_confirmed:
            # Rescale the extrapolated power law to anchor exactly to the lowest known confirmed level
            anchor_level = min_known_confirmed
            anchor_value = exact_formulas[anchor_level]["start"]
            scale = anchor_value / power_law(anchor_level, extrapolate_A, extrapolate_B)
            
            start = power_law(lvl, extrapolate_A, extrapolate_B) * scale
            next_start = power_law(lvl + 1, extrapolate_A, extrapolate_B) * scale
            
            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False,
                "extrapolated": True
            }"""

code = code.replace(old_loop, new_loop)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
