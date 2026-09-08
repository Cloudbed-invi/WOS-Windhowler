with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("min(known_levels) if known_levels else 1", "min(known_levels) if len(known_levels) > 0 else 1")

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
