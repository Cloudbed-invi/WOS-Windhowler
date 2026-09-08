with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_flag = """with tab_flag:
    st.subheader("Needs Review (Flagged OCR & Syncs)")
    if os.path.exists("needs_review.csv"):"""

new_flag = """with tab_flag:
    st.subheader("Needs Review (Flagged OCR & Syncs)")
    st.info("ℹ️ **Note on Baseline Poisoning:** A 'window shift' flag means the submission disagrees with the current confirmed baseline. If that baseline only has 2-3 points, it might be the baseline itself that was built on a mismatched account. A human must judge which side is actually correct.")
    if os.path.exists("needs_review.csv"):"""

code = code.replace(old_flag, new_flag)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    pipe = f.read()

old_cmt = """    Temporarily refits the Huber regression for a confirmed level including the new point.
    Returns the percentage shift in the window coefficient.
    \"\"\""""

new_cmt = """    Temporarily refits the Huber regression for a confirmed level including the new point.
    Returns the percentage shift in the window coefficient.
    Note: A large shift just means it disagrees with the baseline. If the baseline 
    only has 2 points from a bad account, the baseline itself is poisoned. This check 
    flags the disagreement so a human can resolve it.
    \"\"\""""

pipe = pipe.replace(old_cmt, new_cmt)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(pipe)
