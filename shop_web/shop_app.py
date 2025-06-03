from flask import Flask, request, render_template, jsonify
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar

app = Flask(
    __name__,
    static_folder='shop_web/static',
    template_folder='shop_web/template'
)

@app.route('/')
def index():
    """
    QRコード読み取り画面を表示
    """
    return render_template('qr_reader.html')

@app.route('/scan', methods=['POST'])
def scan():
    """
    QRコード画像を受け取り、デコードして結果を返す
    """
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
            return jsonify({"success": False, "error": "QRコードが検出できませんでした"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/success')
def success():
    """
    QRコード読み取り成功画面
    """
    return render_template('success.html')

@app.route('/failure')
def failure():
    """
    QRコード読み取り失敗画面
    """
    return render_template('failure.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)