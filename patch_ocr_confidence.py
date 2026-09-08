import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove 'ch_sim' to prevent EasyOCR from splitting probabilities with Chinese characters
code = code.replace("easyocr.Reader(['en', 'ch_sim'], gpu=True)", "easyocr.Reader(['en'], gpu=True)")

# 2. Add Binary Thresholding to OpenCV preprocessing
old_cv2 = """    # PHASE 1: CLAHE Contrast Enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    optimized_path = img_path + "_opt.jpg"
    cv2.imwrite(optimized_path, enhanced)"""

new_cv2 = """    # PHASE 1: CLAHE Contrast Enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # PHASE 1.5: Otsu's Binary Thresholding (Pure Black & White)
    # This removes all background noise and makes text perfectly crisp for EasyOCR
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    optimized_path = img_path + "_opt.jpg"
    cv2.imwrite(optimized_path, thresh)"""

code = code.replace(old_cv2, new_cv2)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
