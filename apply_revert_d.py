with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_info = """    st.info("ℹ️ **Note on Baseline Poisoning:** A 'window shift' flag means the submission disagrees with the current confirmed baseline. If that baseline only has 2-3 points, it might be the baseline itself that was built on a mismatched account. A human must judge which side is actually correct.")\n"""

code = code.replace(old_info, "")

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    pipe = f.read()

old_cmt = """    Note: A large shift just means it disagrees with the baseline. If the baseline 
    only has 2 points from a bad account, the baseline itself is poisoned. This check 
    flags the disagreement so a human can resolve it."""

new_cmt = """    Note: Since the baseline data is strictly verified, a large shift 
    indicates the incoming submission is a vast outlier (e.g. from a different account)."""

pipe = pipe.replace(old_cmt, new_cmt)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe)
