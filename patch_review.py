import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# We need to update the Review Extracted Data section to handle the new columns
old_review = """# --- REVIEW PENDING OCR ---
if st.session_state.pending_ocr is not None:
    st.write("---")
    st.subheader("🧐 Review Extracted Data")
    st.info("The OCR extracted the following data. Verify it is correct before publishing.")
    
    edited_df = st.data_editor(st.session_state.pending_ocr, num_rows="dynamic")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve & Publish to AI Model", type="primary"):
            # Save approved data to CSV
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": row.get("Name", "Community"),
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"])
                        })
"""

new_review = """# --- REVIEW PENDING OCR ---
if st.session_state.pending_ocr is not None:
    st.write("---")
    st.subheader("🧐 Review Extracted Data")
    
    has_flags = any(r.get("Flag") for r in st.session_state.pending_ocr)
    if has_flags:
        st.warning("⚠️ Some OCR reads were flagged due to low confidence or failing sanity checks. Please review them carefully!")
    else:
        st.info("The OCR extracted the following data. Verify it is correct before publishing.")
        
    edited_df = st.data_editor(st.session_state.pending_ocr, num_rows="dynamic")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve & Publish to AI Model", type="primary"):
            # Save approved data to CSV (ignoring Confidence/Flag columns to keep master data pure)
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": row.get("Name", "Community"),
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"])
                        })
"""

if old_review in code:
    code = code.replace(old_review, new_review)
    with open("admin_dashboard.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Dashboard patched successfully.")
else:
    print("Could not find the review section to patch.")
