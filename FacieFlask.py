from flask import Flask, request, render_template, send_file
from analysis import get_metrics
import os
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        image_file = request.files.get("image")
        if image_file:
            os.makedirs("static", exist_ok=True)
            upload_path = os.path.join("static", "upload.jpg")
            image_file.save(upload_path)

            metrics, pts = get_metrics(upload_path, return_points=True)
            img = cv2.imread(upload_path)

            # Малюємо всі лінії
            pairs = [
                ("left_jaw", "right_jaw", (255, 0, 0)),
                ("left_temple", "right_temple", (0, 255, 255)),
                ("extra_left_1", "extra_right_1", (0, 255, 0)),
                ("extra_left_2", "extra_right_2", (255, 128, 0))
            ]

            for left_key, right_key, color in pairs:
                if left_key in pts and right_key in pts:
                    pt1 = tuple(map(int, pts[left_key]))
                    pt2 = tuple(map(int, pts[right_key]))
                    cv2.circle(img, pt1, 5, color, -1)
                    cv2.circle(img, pt2, 5, color, -1)
                    cv2.line(img, pt1, pt2, color, 2)

            result_path = os.path.join("static", "result.jpg")
            cv2.imwrite(result_path, img)

            if "error" in metrics:
                result = {"error": metrics["error"]}
            else:
                ratio = metrics.get("jaw/temple_ratio")
                result = {
                    "class": metrics.get("Тип щелепи", "---"),
                    "ratio": round(ratio, 3) if ratio is not None else "---",
                    "confidence": f"{round(abs(ratio - 0.975), 3)} (до межі)" if ratio else "---",
                    "metrics": metrics
                }

    return render_template("index.html", result=result)

@app.route("/result-image")
def result_image():
    return send_file(os.path.join("static", "result.jpg"), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
