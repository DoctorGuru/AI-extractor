# Leaflet Product Extraction

**Candidate:** Omomoluwa Tobi  
**Position:** AI Developer  

This project implements an end-to-end pipeline that extracts product information from leaflet images, structures it into JSON, and displays it in a clickable web interface.

---

## Overview

The solution:

1. Extracts text from leaflet images using OCR.  
2. Cleans and parses the text into structured product data.  
3. Outputs the data as a JSON file.  
4. Provides a local web application to display products interactively.

---

## OCR Extraction

- **Tool:** Tesseract OCR (`pytesseract`)  
- **Image Preprocessing:**  
  - Convert to grayscale  
  - Apply Gaussian blur to reduce noise  
  - Adaptive thresholding for better text recognition  
  - Resize to improve OCR accuracy  

- **Output:** OCR text is saved as `.txt` files for debugging and stored in a dictionary for parsing.

---

## Text Parsing & Cleaning

- **Cleaning:** Fixes common OCR errors and removes unwanted symbols.  
- **Parsing:**  
  - Identifies numbers as potential prices.  
  - Text preceding numbers treated as product names.  
  - Trailing units (per, pk, g, kg, litre, c, pack) removed.  

- **Example Output:**
```json
{
  "leaflet1.jpg": [{"name": "BANANA BREAD", "price": "2"}],
  "leaflet2.jpg": [{"name": "BLACK BEANS", "price": "600"}]
}

## Web Application Interface

**Framework:** Flask

**Features:**

- Displays all products from all leaflets in a table.
- Each row is clickable to simulate product selection.
- Selected products are saved to `selected_product.json`.
- Provides REST API endpoint `/api/products` to access JSON product data.
- Simple and extendable interface for filtering, sorting, or additional features.

**Template:**

- HTML template (`templates/index.html`) renders the product table.
- JavaScript handles row clicks and POST requests to `/select_product`.
- Provides immediate visual feedback for selected products.

## Generate OCR & JSON
- python app.py

## Run Web Interface
- python web_app.py


