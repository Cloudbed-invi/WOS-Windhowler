with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_exact_assignment = """        exact_formulas[int(lvl)] = {
            "start": round(start_damage),
            "window": round(window_size),
            "confirmed": True
        }"""

new_exact_assignment = """        pct_spread = level_data["Percent"].max() - level_data["Percent"].min()
        is_strong = bool(pct_spread >= 25.0)

        exact_formulas[int(lvl)] = {
            "start": round(start_damage),
            "window": round(window_size),
            "confirmed": is_strong,
            "clustered": not is_strong
        }"""

code = code.replace(old_exact_assignment, new_exact_assignment)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
