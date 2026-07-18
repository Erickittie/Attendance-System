import easyocr
import re

# Load OCR model once
reader = easyocr.Reader(['en'])

def detect_id_number(image):
    """
    Detects a 10-digit student ID number from an image.
    Returns the ID number if found, otherwise None.
    """

    results = reader.readtext(image)

    for result in results:

        text = result[1]

        # Remove spaces
        text = text.replace(" ", "")

        # Find a 10-digit number
        match = re.search(r"\b\d{10}\b", text)

        if match:
            return match.group()

    return None