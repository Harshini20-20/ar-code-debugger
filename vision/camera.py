import cv2
from ocr.extract_text import extract_text
from utils.text_cleaner import clean_code
from debugger.syntax_checker import check_syntax


def start_camera():

    # 📱 IP Webcam URL (CHANGE if your IP changes)
    url = "http://192.168.1.16:8080/video"

    # 🎥 Open stream
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    error_line = None
    error = None
    boxes = []

    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return

    print("✅ Camera started. Press 'S' to scan, 'Q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("⚠️ Frame dropped... retrying")
            continue

        # 🟥 Draw error overlay
        if error_line is not None and error is not None and error_line < len(boxes):

            box = boxes[error_line]

            x1, y1 = int(box[0][0]), int(box[0][1])
            x2, y2 = int(box[2][0]), int(box[2][1])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            cv2.putText(
                frame,
                error,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )
        frame = cv2.resize(frame, (640, 480))   # smaller size
        cv2.imshow("AR Debugger - Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        # 📸 Press S to scan code
        if key == ord('s'):

            image_path = "captured_code.png"

            h, w, _ = frame.shape

            # ✂️ Crop center region
            crop = frame[int(h * 0.35):int(h * 0.75),
                         int(w * 0.15):int(w * 0.85)]

            # ⚫ Convert to grayscale
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            cv2.imwrite(image_path, gray)

            print("\n📸 IMAGE CAPTURED!")

            # 🔍 OCR
            ocr_lines = extract_text(image_path)

            texts = []
            boxes = []

            for item in ocr_lines:
                texts.append(item["text"])
                boxes.append(item["bbox"])

            cleaned = clean_code(texts)

            print("\n🧾 Detected text:")
            for line in cleaned:
                print(line)

            # 🐞 Syntax check
            error = check_syntax(cleaned)

            print("\n🛠 DEBUG RESULT:")
            print(error)

            # 🔍 Extract error line
            error_line = None
            if error and "line" in error:
                try:
                    error_line = int(
                        error.split("line")[1].split(":")[0].strip()
                    ) - 1
                except:
                    error_line = None

        # ❌ Quit
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()