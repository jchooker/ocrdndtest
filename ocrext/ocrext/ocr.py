import pytesseract
import shutil
import os
from PIL import Image

#set path to tesseract (adjust if installed elsewhere)
#make tesseract.exe future-proof and available now w/o PATH being previously set
def get_tesseract_path():
    """Attempts to find Tesseract in common install locations or PATH."""
    possible_paths = [
        r"C:\\Program Files\\Tesseract\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract\\tesseract.exe"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
        
    #try to detect it dynamically
    try:
        tesseract_path = shutil.which("tesseract")
        if not tesseract_path:
            raise FileNotFoundError("Tesseract is not installed or not in PATH.")
    except Exception as e:
        print(f"⚠️ {e}")
        print("Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
    else:
        print(f"✅ Tesseract found at: {tesseract_path}")

#     try:
#         pytesseract.pytesseract.tesseract_cmd = f"C:\Program Files\Tesseract-OCR\\tesseract.exe"
#         if not pytesseract.pytesseract.tesseract_cmd:
#             print(f"Pytesseract not found on static path of: {pytesseract.pytesseract.tesseract_cmd}")
#     except Exception as e:
#         print(f"Exception while trying to find Pytesseract on static path: {pytesseract.pytesseract.tesseract_cmd}")

# try:
#     tesseract_path = shutil.which("tesseract")
#     if tesseract_path:
#         pytesseract.pytesseract.tesseract_cmd = tesseract_path
#     else:
#         raise FileNotFoundError("Tesseract not found! Ensure it is installed and in PATH.")
# except Exception as e:
#     print(f"Exception while trying to find Pytesseract on PATH: {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def extract_text(image_path):
    """Extract text from an image using tesseract ocr"""
    img = Image.open(image_path)
    img = img.convert("RGB")
    print(f"Type of img: {type(img)}")  # Should be <class 'PIL.Image.Image'>
    print(f"Image mode: {img.mode}")  # Should be RGB or grayscale
    print(f"Image size: {img.size}")  # Should be non-zero
    print(f"Tesseract Path: {pytesseract.pytesseract.tesseract_cmd}")
    text = pytesseract.image_to_string(img)
    return text