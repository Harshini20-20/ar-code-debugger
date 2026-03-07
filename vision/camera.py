import cv2
from ocr.extract_text import extract_text
from utils.text_cleaner import clean_code
from debugger.syntax_checker import check_syntax


def start_camera():

    cap = cv2.VideoCapture(0)

    error_line = None
    boxes = []

    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Draw error overlay if available
        if error_line is not None and error_line < len(boxes):

            box = boxes[error_line]

            x = int(box[0][0])
            y = int(box[0][1])

            cv2.rectangle(frame, (x-10, y-10), (x+300, y+30), (0,0,255), 2)

            cv2.putText(frame,error,(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

        cv2.imshow("AR Debugger - Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        # Press S to scan code
        if key == ord('s'):

            image_path = "captured_code.png"

            # Get frame dimensions
            h, w, _ = frame.shape

            # Crop center region where code is likely located
            crop = frame[int(h*0.35):int(h*0.75), int(w*0.15):int(w*0.85)]

            # Convert cropped region to grayscale
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            # Save the processed image
            cv2.imwrite(image_path, gray)

            print("IMAGE CAPTURED!")

            ocr_lines = extract_text(image_path)

            texts = []
            boxes = []

            for item in ocr_lines:
                texts.append(item["text"])
                boxes.append(item["bbox"])

            cleaned = clean_code(texts)

            print("\nDetected text:")
            for line in cleaned:
                print(line)

            error = check_syntax(cleaned)

            print("\nDEBUG RESULT:")
            print(error)

            # detect line number
            if "line" in error:
                try:
                    error_line = int(error.split("line")[1].split(":")[0].strip()) - 1
                except:
                    error_line = None

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()