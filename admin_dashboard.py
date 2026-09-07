import streamlit as st
import os
import subprocess
import time
import base64
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

st.write("Upload or paste screenshots to calculate exact Boss HP and publish the formulas to GitHub Pages.")

if "pasted_images" not in st.session_state:
    st.session_state.pasted_images = []
if "seen_hashes" not in st.session_state:
    st.session_state.seen_hashes = set()
if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = []

st.subheader("1. Paste Screenshots")
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
        # Create a grid of 8 columns for smaller images
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
st.subheader("Process Previously Saved Images")
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

st.subheader("2. Publish to GitHub Pages")
st.write("Commit the updated exact_levels.js and HTML file to your repository so visitors see the latest formulas.")
if st.button("🚀 Commit & Push to GitHub"):
    try:
        with st.spinner("Pushing to GitHub..."):
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-update exact levels from Admin UI"], check=True)
            subprocess.run(["git", "push"], check=True)
        st.success("✅ Successfully published to GitHub Pages!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to push to GitHub. Error: {e}")
