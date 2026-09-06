import streamlit as st
import os
import subprocess
import time
import wos_pipeline

st.set_page_config(page_title="Windhowler Admin", layout="centered")

st.title("🐺 Windhowler Formula Admin")
st.write("Upload or paste screenshots to calculate exact Boss HP and publish the formulas to GitHub Pages.")

st.subheader("1. Upload Screenshots")
st.info("💡 You can drag & drop multiple files, or click inside the box below and press Ctrl+V to paste images directly from your clipboard!")
uploaded_files = st.file_uploader("Select Battle Reports", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if st.button("Save & Process Images"):
    if uploaded_files:
        wos_pipeline.setup_folders()
        # Save files
        for f in uploaded_files:
            with open(os.path.join("images", f.name), "wb") as out:
                out.write(f.getbuffer())
        st.success(f"Saved {len(uploaded_files)} images!")
        
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
            st.json(results)
    else:
        st.error("Please upload images first.")

st.subheader("2. Publish to GitHub Pages")
st.write("Commit the updated exact_levels.js and HTML file to your repository so visitors see the latest formulas.")
if st.button("🚀 Commit & Push to GitHub"):
    try:
        with st.spinner("Pushing to GitHub..."):
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-update exact levels from Admin UI"], check=True)
            subprocess.run(["git", "push"], check=True)
        st.success("✅ Successfully published to GitHub Pages!")
    except Exception as e:
        st.error(f"Failed to push to GitHub. Error: {e}")
