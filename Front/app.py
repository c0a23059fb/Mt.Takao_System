from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.get_json()
    image_data = data.get('image')
    # ここで画像データをDBの写真と照合し、判定する処理を実装
    # 仮で一致した場合はsuccess: Trueを返す
    # 実際の照合ロジックは別途実装してください
    if image_data:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)