import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's insert the table into the Data Coverage tab
old_tab = """            def highlight_low(row):
                color = 'background-color: #ffcccc; color: #900' if row['Confirmed Points'] < 3 else ''
                return [color]*len(row)
            st.dataframe(df_cov.style.apply(highlight_low, axis=1), height=400, use_container_width=True)
        else:
            st.write("data.csv is empty.")
    else:
        st.write("data.csv not found.")"""

new_tab = """            def highlight_low(row):
                color = 'background-color: #ffcccc; color: #900' if row['Confirmed Points'] < 3 else ''
                return [color]*len(row)
            st.dataframe(df_cov.style.apply(highlight_low, axis=1), height=400, use_container_width=True)
        else:
            st.write("data.csv is empty.")
    else:
        st.write("data.csv not found.")
        
    st.divider()
    st.subheader("Adjacent Huber Fit Mismatches")
    st.write("Diagnostic check: validates if the end of level N perfectly connects to the start of level N+1 using the raw Huber Regression data.")
    
    import wos_pipeline
    config = wos_pipeline.load_formulas()
    mismatches = config.get("ADJACENT_MISMATCHES", [])
    
    if mismatches:
        df_mis = pd.DataFrame(mismatches)
        def highlight_mismatch(row):
            color = 'background-color: #ffcccc; color: #900' if row['Flagged'] else ''
            return [color]*len(row)
        st.dataframe(df_mis.style.apply(highlight_mismatch, axis=1), use_container_width=True)
    else:
        st.success("No adjacent pairs found to check.")"""

code = code.replace(old_tab, new_tab)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

