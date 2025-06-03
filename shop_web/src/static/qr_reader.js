let stream = null; // カメラストリームを保持
let qrScanInterval = null; // QRコードスキャン用のタイマー

async function startCamera() {
  try {
    const video = document.getElementById('video');
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: { exact: "environment" } // 外カメラを指定
      }
    });
    video.srcObject = stream;

    // QRコードスキャンを開始
    startQRScan();
  } catch (error) {
    console.error('カメラを起動できませんでした:', error);
    alert(`カメラを起動できませんでした。エラー内容: ${error.message}`);
  }
}

function stopCamera() {
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop()); // カメラを停止
    stream = null;
    const video = document.getElementById('video');
    video.srcObject = null; // ビデオストリームを解除
  }

  // QRコードスキャンを停止
  stopQRScan();
}

function toggleCamera() {
  const button = document.getElementById('camera-toggle');
  if (stream) {
    stopCamera();
    button.textContent = "カメラ起動";
  } else {
    startCamera();
    button.textContent = "カメラ停止";
  }
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