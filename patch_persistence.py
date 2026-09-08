import re
import os

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove session state initialization for pending_ocr
code = code.replace("""if "pending_ocr" not in st.session_state:
    st.session_state.pending_ocr = None""", """import json
def get_pending_ocr():
    if os.path.exists("pending_ocr.json"):
        try:
            with open("pending_ocr.json", "r") as f:
                return json.load(f)
        except:
            return None
    return None

def clear_pending_ocr():
    if os.path.exists("pending_ocr.json"):
        os.remove("pending_ocr.json")""")

# 2. Update saving new_entries to pending_ocr.json instead of session state
code = code.replace("""        if isinstance(new_entries, list) and len(new_entries) > 0:
            st.session_state.pending_ocr = new_entries
        else:
            st.warning("No readable data could be extracted from those images.")
            st.session_state.pending_ocr = None""", """        if isinstance(new_entries, list) and len(new_entries) > 0:
            with open("pending_ocr.json", "w") as f:
                json.dump(new_entries, f)
        else:
            st.warning("No readable data could be extracted from those images.")
            clear_pending_ocr()""")

# 3. Update the review section to read from function
code = code.replace("""# --- REVIEW PENDING OCR ---
if st.session_state.pending_ocr is not None:""", """# --- REVIEW PENDING OCR ---
pending_data = get_pending_ocr()
if pending_data is not None:""")

# 4. Replace remaining session_state.pending_ocr with pending_data
code = code.replace("""has_flags = any(r.get("Flag") for r in st.session_state.pending_ocr)""", """has_flags = any(r.get("Flag") for r in pending_data)""")
code = code.replace("""edited_df = st.data_editor(st.session_state.pending_ocr, num_rows="dynamic")""", """edited_df = st.data_editor(pending_data, num_rows="dynamic")""")

# 5. Replace clearing state with clearing file
code = code.replace("""st.session_state.pending_ocr = None""", """clear_pending_ocr()""")

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
