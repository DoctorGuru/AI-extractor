import os
import cv2
import pytesseract
from PIL import Image
from parser.product_parser import parse_products, save_to_json

IMAGES_DIR = "images"
OCR_OUTPUT_DIR = "output/ocr_text"
os.makedirs(OCR_OUTPUT_DIR, exist_ok=True)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    thresh = cv2.resize(thresh, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return Image.fromarray(thresh)

# OCR CONFIG
OCR_CONFIG = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,- '

leaflets = [f for f in os.listdir(IMAGES_DIR) if f.endswith(".jpg")]

raw_texts = {}

for leaflet in leaflets:
    image_path = os.path.join(IMAGES_DIR, leaflet)
    processed_image = preprocess_image(image_path)

    text = pytesseract.image_to_string(processed_image, config=OCR_CONFIG)

    # Save OCR text for debugging
    txt_path = os.path.join(OCR_OUTPUT_DIR, leaflet.replace(".jpg", ".txt"))
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    raw_texts[leaflet] = text
    print(f"OCR extracted: {leaflet}")

# Parse OCR text
products_dict = parse_products(raw_texts)

# Save JSON
save_to_json(products_dict, "output/data.json")

print("\nFINAL PARSED OUTPUT:")
print(products_dict)
