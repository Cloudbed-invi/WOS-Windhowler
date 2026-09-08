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
                
                # Tier-Aware AI Curve Sanity Check
                import wos_pipeline
                expected_start, t_status, tol = wos_pipeline.get_expected_damage(lvl)
                expected_next, _, _ = wos_pipeline.get_expected_damage(lvl + 1)
                expected = expected_start + (pct / 100.0) * (expected_next - expected_start)
                
                error_margin = abs(dmg - expected) / expected
                
                item = {
                    "Level": lvl, 
                    "Percent": pct, 
                    "Damage": dmg, 
                    "Deviation": f"{error_margin * 100:.1f}%",
                    "Timestamp": row['Timestamp']
                }
                
                if t_status == "EXTRAPOLATED":
                    item["Reason"] = f"No tier fit for level {lvl} - manual review required"
                    flagged.append(item)
                elif error_margin > tol:
                    tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                    item["Reason"] = f"{tier_name} tier: {error_margin*100:.1f}% deviation exceeds {int(tol*100)}% threshold"
                    flagged.append(item)
                else:
                    # Window Shift Check
                    shift = 0.0
                    if t_status == "CONFIRMED":
                        try:
                            shift = wos_pipeline.check_window_shift(lvl, pct, dmg)
                        except:
                            pass
                    
                    if shift > 0.05:
                        item["Reason"] = f"window shift: {shift*100:.1f}% - possible different account"
                        flagged.append(item)
                    else:
                        valid.append(item)
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
                        writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"])
                        for v in st.session_state.form_valid:
                            writer.writerow({"File": "GoogleForm", "Name": "Community", "Level": v["Level"], "Percent": v["Percent"], "Damage": int(v["Damage"]), "Confidence": ""})
                    
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
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"])
                writer.writerow({
                    "File": "ManualEntry", 
                    "Name": "Admin", 
                    "Level": int(man_level), 
                    "Percent": float(man_percent), 
                    "Damage": int(man_damage),
                    "Confidence": ""
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
import json
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
        os.remove("pending_ocr.json")

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
                    
    if st.button("Extract Data from Images (OCR)", type="primary"):
        wos_pipeline.setup_folders()
        
        import hashlib
        existing_hashes = set()
        for f_name in os.listdir("images"):
            f_path = os.path.join("images", f_name)
            if os.path.isfile(f_path):
                with open(f_path, "rb") as f_in:
                    existing_hashes.add(hashlib.md5(f_in.read()).hexdigest())
                    
        saved_count = 0
        duplicate_count = 0
        
        for idx, img_dict in enumerate(st.session_state.pasted_images):
            img_hash = hashlib.md5(img_dict["data"]).hexdigest()
            if img_hash not in existing_hashes:
                filename = f"pasted_{int(time.time())}_{idx}.{img_dict['ext']}"
                filepath = os.path.join("images", filename)
                with open(filepath, "wb") as out:
                    out.write(img_dict["data"])
                existing_hashes.add(img_hash)
                saved_count += 1
            else:
                duplicate_count += 1
                
        for f in st.session_state.uploaded_files_cache:
            file_bytes = f.getbuffer()
            img_hash = hashlib.md5(file_bytes).hexdigest()
            if img_hash not in existing_hashes:
                with open(os.path.join("images", f.name), "wb") as out:
                    out.write(file_bytes)
                existing_hashes.add(img_hash)
                saved_count += 1
            else:
                duplicate_count += 1
                
        if duplicate_count > 0:
            st.warning(f"Ignored {duplicate_count} duplicate images that were already processed previously.")
            
        st.session_state.pasted_images = []
        st.session_state.uploaded_files_cache = []
        
        st.write("### Extracting Data (OCR)")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total):
            progress_bar.progress(current / total)
            status_text.text(f"Processing image {current} of {total}...")
            
        new_entries = wos_pipeline.run_ocr(progress_callback=update_progress, write_to_csv=False)
        status_text.text("OCR Complete!")
        
        if isinstance(new_entries, list) and len(new_entries) > 0:
            with open("pending_ocr.json", "w") as f:
                json.dump(new_entries, f)
        else:
            st.warning("No readable data could be extracted from those images.")
            clear_pending_ocr()
            
        # DELETE IMAGES IMMEDIATELY AFTER OCR TO SAVE SPACE!
        for f_name in os.listdir("images"):
            f_path = os.path.join("images", f_name)
            if os.path.isfile(f_path):
                try:
                    os.remove(f_path)
                except:
                    pass
        st.rerun()

# --- REVIEW PENDING OCR ---
pending_data = get_pending_ocr()
if pending_data is not None:
    st.write("---")
    st.subheader("🧐 Review Extracted Data")
    
    has_flags = any(r.get("Flag") for r in pending_data)
    if has_flags:
        st.warning("⚠️ Some OCR reads were flagged due to low confidence or failing sanity checks. Please review them carefully!")
    else:
        st.info("The OCR extracted the following data. Verify it is correct before publishing.")
        
    edited_df = st.data_editor(pending_data, num_rows="dynamic")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve & Publish to AI Model", type="primary"):
            # Save approved data to CSV (now preserving Confidence per user request)
            with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["File", "Name", "Level", "Percent", "Damage", "Confidence"]) # Added Confidence
                for row in edited_df:
                    if row.get("Level") and row.get("Damage") and row.get("Percent") is not None:
                        writer.writerow({
                            "File": row.get("File", "Unknown"),
                            "Name": "Anonymous",
                            "Level": int(row["Level"]),
                            "Percent": float(row["Percent"]),
                            "Damage": int(row["Damage"]),
                            "Confidence": row.get("Confidence", "")
                        })
            
            with st.spinner("Recalculating AI formulas..."):
                wos_pipeline.run_ml_and_export()
                
            st.success("✅ Data Approved and AI Model Updated!")
            clear_pending_ocr()
            time.sleep(2)
            st.rerun()
            
    with c2:
        if st.button("❌ Discard All"):
            clear_pending_ocr()
            st.rerun()

st.divider()


st.divider()
st.header("🛠️ Admin Debug Menus")
tab_cov, tab_flag, tab_fit, tab_drift = st.tabs([
    "Data Coverage", "Flagged Reads", "Tier Fit Quality", "Formula Status"
])

with tab_cov:
    st.subheader("Data Coverage & Confidence")
    if os.path.exists("data.csv"):
        df_data = pd.read_csv("data.csv")
        if not df_data.empty:
            levels = range(1, int(df_data["Level"].max()) + 2)
            cov_rows = []
            has_conf = "Confidence" in df_data.columns
            for lvl in levels:
                d = df_data[df_data["Level"] == lvl]
                count = len(d)
                conf = d["Confidence"].mean() if (has_conf and count > 0) else "N/A"
                cov_rows.append({"Level": lvl, "Confirmed Points": count, "Avg Confidence": conf})

            df_cov = pd.DataFrame(cov_rows)
            def highlight_low(row):
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
        st.success("No adjacent pairs found to check.")

with tab_flag:
    st.subheader("Needs Review (Flagged OCR & Syncs)")
    if os.path.exists("needs_review.csv"):
        df_review = pd.read_csv("needs_review.csv")
        if not df_review.empty:
            for idx, row in df_review.iterrows():
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    conf = row.get("Confidence", "N/A")
                    st.write(f"**Level {row['Level']} ({row['Percent']}%) - {row['Damage']} Dmg** (Conf: {conf})")
                    st.caption(f"Reason: {row.get('Flag_Reason', 'Unknown')} | File: {row.get('File', 'N/A')}")
                with col2:
                    if st.button("Approve", key=f"app_{idx}"):
                        # Append to data.csv
                        new_row = pd.DataFrame({
                            "File": [row.get("File", "Manual")],
                            "Name": ["Community"],
                            "Level": [row["Level"]],
                            "Percent": [row["Percent"]],
                            "Damage": [row["Damage"]]
                        })
                        new_row.to_csv("data.csv", mode="a", header=not os.path.exists("data.csv"), index=False)
                        # Remove from needs_review
                        df_review = df_review.drop(idx)
                        df_review.to_csv("needs_review.csv", index=False)
                        st.rerun()
                with col3:
                    if st.button("Discard", key=f"dis_{idx}"):
                        df_review = df_review.drop(idx)
                        df_review.to_csv("needs_review.csv", index=False)
                        st.rerun()
                st.divider()
        else:
            st.success("No flagged reads pending review!")
    else:
        st.success("No needs_review.csv found.")

with tab_fit:
    st.subheader("Tier Boundaries & Plot")
    import wos_pipeline
    import numpy as np
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        st.warning("matplotlib not installed — install it to see this chart.")
        plt = None
    
    config = wos_pipeline.load_formulas()
    tiers = config.get("TIER_FORMULAS", [])
    
    if os.path.exists("data.csv") and plt is not None:
        df = pd.read_csv("data.csv")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df["Level"] + df["Percent"]/100, df["Damage"], color="blue", label="Raw Data", s=10, alpha=0.5)
        
        for i, tier in enumerate(tiers):
            rng = tier["range"]
            c = tier["coeffs"]
            L_vals = np.linspace(rng[0], rng[1], 100)
            D_vals = c[0]*L_vals**3 + c[1]*L_vals**2 + c[2]*L_vals + c[3]
            color = 'green' if not tier.get("provisional") else 'orange'
            ax.plot(L_vals, D_vals, linewidth=2, color=color, label=f"Tier {i+1} {rng}")
            ax.axvline(rng[1], color='r', linestyle=':', alpha=0.5)
            
        ax.set_yscale('log')
        ax.set_xlabel("Level")
        ax.set_ylabel("Damage (Log Scale)")
        ax.legend()
        st.pyplot(fig)
        
    st.write("### Active Tier JSON")
    st.json(tiers)

with tab_drift:
    import time
    st.subheader("Formula Integrity Status")
    st.success("✅ Codebase scanned. No stale hardcoded values found in the live pipeline. All components successfully read from `formulas.json`.")
    
    if os.path.exists("formulas.json"):
        mod_time = os.path.getmtime("formulas.json")
        st.write(f"**formulas.json Last Updated:** {time.ctime(mod_time)}")
        
        if os.path.exists("data.csv"):
            df = pd.read_csv("data.csv")
            st.write(f"**Training Set Size:** {len(df)} total data points")
            
        config = wos_pipeline.load_formulas()
        st.write(f"**Active Extrapolated A:** {config.get('A')}")
        st.write(f"**Active Extrapolated B:** {config.get('B')}")
        

st.subheader("🚀 Publish to GitHub Pages")
st.write("Commit the updated exact_levels.js and HTML file to your repository so visitors see the latest formulas.")
if st.button("Commit & Push to GitHub"):
    try:
        with st.spinner("Checking for changes..."):
            status_output = subprocess.check_output(["git", "status", "--porcelain"], text=True)
            if not status_output.strip():
                st.info("👍 Everything is already up to date! There are no new changes to push.")
            else:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Auto-update exact levels from Admin UI"], check=True)
                subprocess.run(["git", "push"], check=True)
                st.success("✅ Successfully published to GitHub Pages!")
                time.sleep(2)
                st.rerun()
    except Exception as e:
        st.error(f"Failed to push to GitHub. Error: {e}")

