import easyocr
import cv2

reader = easyocr.Reader(["en"], gpu=True)
results = reader.readtext(r"C:\Users\sriha\.gemini\antigravity\brain\b05984a9-a0b3-48ba-becf-1d38d7764a74\.user_uploaded\media_1788925051804.png", detail=1)

full_text = " ".join([res[1] for res in results])
print("OCR TEXT:", full_text)
