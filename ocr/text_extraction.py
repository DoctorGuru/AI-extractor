import pytesseract
from .image_preprocessing import preprocess_images_in_folder

def extract_text_from_images(folder_path):
    processed_images = preprocess_images_in_folder(folder_path)
    extracted_texts = {}

    for filename, image in processed_images.items():
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_texts[filename] = text

    return extracted_texts
