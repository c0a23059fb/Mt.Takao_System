let stream = null; // カメラストリームを保持
let qrScanInterval = null; // QRコードスキャン用のタイマー
let videoStream = null;

// カメラを起動する関数
function toggleCamera() {
  const video = document.getElementById('video');
  if (!videoStream) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoStream = stream;
        video.srcObject = stream;

        // QRコードスキャンを開始
        startQRScan();
      })
      .catch((error) => {
        console.error('カメラを起動できませんでした:', error);
        alert(`カメラを起動できませんでした。エラー内容: ${error.message}`);
      });
  } else {
    stopCamera();
  }
}

// カメラを停止する関数
function stopCamera() {
  if (videoStream) {
    const tracks = videoStream.getTracks();
    tracks.forEach((track) => track.stop()); // カメラを停止
    videoStream = null;
    const video = document.getElementById('video');
    video.srcObject = null; // ビデオストリームを解除
  }

  // QRコードスキャンを停止
  stopQRScan();
}

function startQRScan() {
  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');

  qrScanInterval = setInterval(() => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, canvas.width, canvas.height);

    if (code) {
      alert(`QRコードを読み取りました: ${code.data}`);
      stopCamera(); // QRコードを読み取ったらカメラを停止
    }
  }, 500); // 500msごとにスキャン
}

function stopQRScan() {
  if (qrScanInterval) {
    clearInterval(qrScanInterval);
    qrScanInterval = null;
  }
}

function navigateToHome() {
  stopCamera(); // ホーム画面に戻る前にカメラを停止
  window.location.href = "/";
}

// ページを離れる際にカメラを停止
window.addEventListener('pagehide', stopCamera);

// 写真を撮影する関数
function capturePhoto() {
  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');

  // Canvasのサイズをビデオと同じに設定
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  // Canvasにビデオの現在のフレームを描画
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // 画像データをBase64形式に変換
  const imageData = canvas.toDataURL('image/png');

  // サーバーに送信
  fetch('/upload_photo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: imageData }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert('写真を保存しました！');
      } else {
        alert('写真の保存に失敗しました。');
      }
    })
    .catch((error) => {
      console.error('エラーが発生しました:', error);
      alert('エラーが発生しました。');
    });
}