import easyocr
import re


reader = easyocr.Reader(
    ['en']
)



def detect_id_number(image):

    results = reader.readtext(image)


    print("===================")


    for box, text, confidence in results:

        print(
            "OCR:",
            text,
            "Confidence:",
            confidence
        )


        # remove spaces and symbols
        clean_text = re.sub(
            r'\D',
            '',
            text
        )


        # Student ID format: 10 digits
        match = re.search(
            r'\d{10}',
            clean_text
        )


        if match:

            print(
                "FOUND ID:",
                match.group()
            )

            return match.group()


    print("NO ID FOUND")


    return None