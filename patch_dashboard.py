import re

with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# We need to completely rewrite the SCREENSHOT PROCESSING section.
# We'll locate the start of it and replace everything downwards.

start_marker = "# --- SCREENSHOT PROCESSING ---"
end_marker = "# --- SCREENSHOT PROCESSING END ---" # Doesn't exist, we replace till the end of the file except the Github publish part

split_parts = code.split(start_marker)
top_half = split_parts[0]

new_screenshot_section = """# --- SCREENSHOT PROCESSING ---
if "pasted_images" not in st.session_state:
    st.session_state.pasted_images = []
if "seen_hashes" not in st.session_state:
    st.session_state.seen_hashes = set()
if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = []
if "pending_ocr" not in st.session_state:
    st.session_state.pending_ocr = None

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
            
        new_entries = wos_pipeline.run_ocr(progress_callback=update_progress)
        status_text.text("OCR Complete!")
        
        if isinstance(new_entries, list) and len(new_entries) > 0:
            st.session_state.pending_ocr = new_entries
        else:
            st.warning("No readable data could be extracted from those images.")
            st.session_state.pending_ocr = None
            
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
            
            with st.spinner("Recalculating AI formulas..."):
                wos_pipeline.run_ml_and_export()
                
            st.success("✅ Data Approved and AI Model Updated!")
            st.session_state.pending_ocr = None
            time.sleep(2)
            st.rerun()
            
    with c2:
        if st.button("❌ Discard All"):
            st.session_state.pending_ocr = None
            st.rerun()

st.divider()

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
"""

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(top_half + new_screenshot_section)
