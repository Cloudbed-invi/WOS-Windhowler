with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_fit = """    try:
        huber = HuberRegressor().fit(X_new, y_new)
        new_window = huber.coef_[0]
        shift = abs(new_window - old_window) / old_window"""

new_fit = """    try:
        y_scaled = y_new / 1_000_000.0
        huber = HuberRegressor(epsilon=1.35).fit(X_new, y_scaled)
        new_window = huber.coef_[0] * 1_000_000.0
        shift = abs(new_window - old_window) / old_window"""

code = code.replace(old_fit, new_fit)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
