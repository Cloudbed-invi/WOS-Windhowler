import streamlit as st
import os
import subprocess
import time
import base64
import csv
import pandas as pd
import wos_pipeline
from paste_component import paste_listener

st.set_page_config(page_title="Windhowler Admin", layout="wide")

st.title("🐺 Windhowler Formula Admin")

# --- GIT & STORAGE STATS ---
st.write("---")
col1, col2, col3 = st.columns(3)
try:
    if not os.path.exists("images"): os.makedirs("images")
    total_imgs = len([f for f in os.listdir("images") if f.endswith(('.png', '.jpg'))])
    
    status_output = subprocess.check_output(["git", "status", "--porcelain"], text=True)
    uncommitted_files = len(status_output.strip().split('\n')) if status_output.strip() else 0
    
    col1.metric("Total Saved Images", total_imgs)
    col2.metric("Uncommitted Git Changes", f"{uncommitted_files} files" if uncommitted_files else "Up to date!")
except Exception as e:
    pass
st.write("---")

# --- GOOGLE FORMS SYNC ---
st.subheader("☁️ Sync Google Form Data")
st.write("Automatically pull crowdsourced data, filter spam/anomalies, and safely merge valid data.")

if st.button("Fetch & Analyze Responses"):
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2MIT0sNjUKfRdgDneALxVqe7cT7k5fwsdpD76U36NoZD49E__8S2HXeTzcuA0AfyZGqD1InShL3v/pub?output=csv"
        df_form = pd.read_csv(url)
        
        valid = []
        flagged = []
        
        # Load existing data to prevent showing duplicates
        existing_df = pd.read_csv("data.csv") if os.path.exists("data.csv") else pd.DataFrame(columns=["Level", "Percent", "Damage"])
        
        for _, row in df_form.iterrows():
            try:
                lvl = int(row['Trial Level'])
                pct = float(row['Percentage '])
                dmg = float(str(row['Damage Dealt ']).replace(',', '').strip())
                
                # Check if this exact data point already exists in our data.csv
                is_duplicate = ((existing_df['Level'] == lvl) & (existing_df['Percent'] == pct) & (existing_df['Damage'] == dmg)).any()
                if is_duplicate:
                    continue
                
                # AI Curve Sanity Check (Power Law: 844.19 * L^4.0878)
                start = 844.19 * (lvl ** 4.0878)
                next_start = 844.19 * ((lvl + 1) ** 4.0878)
                expected = start + (pct / 100.0) * (next_start - start)
                
                error_margin = abs(dmg - expected) / expected
                
                item = {
                    "Level": lvl, 
                    "Percent": pct, 
                    "Damage": dmg, 
                    "Deviation": f"{error_margin * 100:.1f}%",
                    "Timestamp": row['Timestamp']
                }
                
                # 15% tolerance for new submissions
                if error_margin <= 0.15:
                    valid.append(item)
                else:
                    flagged.append(item)
            except Exception as e:
                continue
                
        st.session_state.form_valid = valid
        st.session_state.form_flagged = flagged
    except Exception as e:
        st.error(f"Failed to fetch Google Forms data: {e}")

if "form_valid" in st.session_state:
    if len(st.session_state.form_valid) > 0 or len(st.session_state.form_flagged) > 0:
        c1, c2 = st.columns(2)
        
        with c1:
            st.success(f"✅ {len(st.session_state.form_valid)} Valid New Submissions (Matches AI Curve)")
            if len(st.session_state.form_valid) > 0:
                st.dataframe(st.session_state.form_valid)
                if st.button("Merge Valid Data & Run ML", type="primary"):
                    with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                        for v in st.session_state.form_valid:
                            writer.writerow({"File": "GoogleForm", "Name": "Community", "Level": v["Level"], "Percent": v["Percent"], "Damage": int(v["Damage"])})
                    
                    st.session_state.form_valid = []
                    
                    with st.spinner("Recalculating AI formulas..."):
                        wos_pipeline.run_ml_and_export()
                    st.success("✅ ML Updated Successfully!")
                    st.rerun()

        with c2:
            if len(st.session_state.form_flagged) > 0:
                st.warning(f"⚠️ {len(st.session_state.form_flagged)} Anomalies Detected (> 15% Deviation)")
                st.write("These submissions were blocked. If you manually verify they are correct, you can add them below.")
                st.dataframe(st.session_state.form_flagged)
    else:
        st.info("No new submissions found since your last sync!")

st.write("---")

# --- MANUAL DATA ENTRY ---
st.subheader("📝 Manually Insert Data")
st.write("Directly add a confirmed data point into the dataset without needing a screenshot.")

with st.form("manual_entry_form", clear_on_submit=True):
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        man_level = st.number_input("Trial Level", min_value=1, step=1)
    with mc2:
        man_percent = st.number_input("Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
    with mc3:
        # Changed to text_input to bypass strict HTML5 numeric validation which blocks commas and steps
        man_damage_str = st.text_input("Damage Dealt", placeholder="e.g. 21,055,194,115")
        
    submit_manual = st.form_submit_button("➕ Add Entry & Update ML", type="primary")
    
    if submit_manual:
        # Safely parse the damage string
        import re
        try:
            digits_only = re.sub(r'[^\d]', '', str(man_damage_str))
            man_damage = int(digits_only) if digits_only else 0
        except:
            man_damage = 0
            
        if man_level > 0 and man_damage > 0:
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage"])
                writer.writerow({
                    "File": "ManualEntry", 
                    "Name": "Admin", 
                    "Level": int(man_level), 
                    "Percent": float(man_percent), 
                    "Damage": int(man_damage)
                })
            
            with st.spinner("Recalculating AI formulas..."):
                wos_pipeline.run_ml_and_export()
            st.success(f"✅ Added Level {man_level} at {man_percent}% with {man_damage:,} Damage and updated formulas!")
        else:
            st.error("Please enter a valid numeric Level and Damage amount.")

st.write("---")

# --- SCREENSHOT PROCESSING ---
if "pasted_images" not in st.session_state:
    st.session_state.pasted_images = []
if "seen_hashes" not in st.session_state:
    st.session_state.seen_hashes = set()
if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = []

st.subheader("📸 Process Screenshots")
st.info("💡 **Magic Paste:** Simply click anywhere on this page and press **Ctrl+V** on your keyboard to paste a screenshot! No popup will open.")

pasted_b64 = paste_listener(key="global_paste")

if pasted_b64:
    header, encoded = pasted_b64.split(",", 1)
    img_data = base64.b64decode(encoded)
    img_hash = hash(encoded)
    
    if img_hash not in st.session_state.seen_hashes:
        st.session_state.seen_hashes.add(img_hash)
        st.session_state.pasted_images.append({
            "hash": img_hash,
            "data": img_data,
            "ext": "png" if "png" in header else "jpg"
        })
        st.rerun()

with st.expander("Or manually upload files (Click here)"):
    uploaded_files = st.file_uploader("Select Battle Reports", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    if uploaded_files:
        st.session_state.uploaded_files_cache = uploaded_files

total_ready = len(st.session_state.pasted_images) + len(st.session_state.uploaded_files_cache)

if total_ready > 0:
    st.write(f"**{total_ready} images ready to process:**")
    
    if st.session_state.pasted_images:
        cols = st.columns(8)
        for idx, img_dict in enumerate(st.session_state.pasted_images):
            with cols[idx % 8]:
                st.image(img_dict["data"], use_container_width=True)
                if st.button("❌", key=f"remove_{idx}", help="Remove image"):
                    st.session_state.pasted_images.pop(idx)
                    st.rerun()
                    
    if st.button("Save & Process Images", type="primary"):
        wos_pipeline.setup_folders()
        
        for idx, img_dict in enumerate(st.session_state.pasted_images):
            filename = f"pasted_{int(time.time())}_{idx}.{img_dict['ext']}"
            filepath = os.path.join("images", filename)
            with open(filepath, "wb") as out:
                out.write(img_dict["data"])
                
        for f in st.session_state.uploaded_files_cache:
            with open(os.path.join("images", f.name), "wb") as out:
                out.write(f.getbuffer())
                
        st.success(f"Saved {total_ready} images!")
        st.session_state.pasted_images = []
        st.session_state.uploaded_files_cache = []
        
        st.write("### Extracting Data (OCR)")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total):
            progress_bar.progress(current / total)
            status_text.text(f"Processing image {current} of {total}...")
            
        wos_pipeline.run_ocr(progress_callback=update_progress)
        status_text.text("OCR Complete!")
        
        st.write("### Running Machine Learning Model")
        with st.spinner("Calculating exact mathematical formulas..."):
            results = wos_pipeline.run_ml_and_export()
            st.success("✅ exact_levels.js updated successfully!")
            
        st.rerun()

st.write("---")
with st.expander("Process Previously Saved Images (Recovery Mode)"):
    st.write("If you already pasted images but the OCR process failed or was interrupted, click below to re-run OCR and Machine Learning on all images currently saved in your `images/` folder.")
    if st.button("Run Pipeline on Saved Images", type="secondary"):
        st.write("### Extracting Data (OCR)")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total):
            progress_bar.progress(current / total)
            status_text.text(f"Processing image {current} of {total}...")
            
        wos_pipeline.run_ocr(progress_callback=update_progress)
        status_text.text("OCR Complete!")
        
        st.write("### Running Machine Learning Model")
        with st.spinner("Calculating exact mathematical formulas..."):
            results = wos_pipeline.run_ml_and_export()
            st.success("✅ exact_levels.js updated successfully!")

st.divider()

st.subheader("🚀 Publish to GitHub Pages")
st.write("Commit the updated exact_levels.js and HTML file to your repository so visitors see the latest formulas.")
if st.button("Commit & Push to GitHub"):
    try:
        with st.spinner("Pushing to GitHub..."):
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-update exact levels from Admin UI"], check=True)
            subprocess.run(["git", "push"], check=True)
        st.success("✅ Successfully published to GitHub Pages!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to push to GitHub. Error: {e}")

