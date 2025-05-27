from flask import Flask, request, jsonify, render_template
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os

app = Flask(
    __name__,
    static_folder='Front/static',
    template_folder='Front/templates'
)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/qr_road')
def qr_road():
    return render_template('qr_road.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    try:
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        decoded_objects = pyzbar.decode(gray)

        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            return jsonify({"success": True, "data": qr_data})
        else:
            return jsonify({"success": False, "error": "No QR code detected"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=('cert.pem', 'key.pem'))