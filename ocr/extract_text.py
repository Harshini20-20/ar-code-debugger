import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image_path):

    results = reader.readtext(image_path)

    lines = []

    for (bbox, text, prob) in results:
        lines.append({
            "text": text,
            "bbox": bbox
        })

    return lines