import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image_path):

    # ✅ FIRST get results
    results = reader.readtext(image_path)

    # ✅ THEN sort them
    results = sorted(results, key=lambda x: x[0][0][1])

    lines = []

    for (bbox, text, prob) in results:
        lines.append({
            "text": text,
            "bbox": bbox
        })

    return lines