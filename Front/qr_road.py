from flask import Flask, request, jsonify, render_template
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    try:
        # リクエストから画像データを取得
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        # QRコード解析
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        decoded_objects = pyzbar.decode(gray)
        if decoded_objects:
            # QRコードに含まれるURLを返す
            qr_data = decoded_objects[0].data.decode('utf-8')
            return jsonify({"success": True, "data": qr_data})
        else:
            return jsonify({"success": False, "error": "No QR code detected"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
