from flask import Flask, request, jsonify, render_template
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import ssl
from dotenv import load_dotenv

app = Flask(
    __name__,
    static_folder='Front/static',
    template_folder='Front/templates'
)


load_dotenv()
cert_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_cert.pem')  # new_cert.pem の絶対パス
key_path = os.path.join(os.path.dirname(__file__), 'keys', 'new_key.pem')   # new_key.pem の絶対パス
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)

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
        print(f"Received data: {data[:100]}")  # デバッグ用ログ（データの先頭100文字を表示）
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
        print(f"Error: {e}")  # デバッグ用ログ
        return jsonify({"success": False, "error": str(e)})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルのディレクトリを取得


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=context)
