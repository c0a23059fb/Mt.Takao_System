let stream = null;
let qrScanInterval = null;

async function startCamera() {
  try {
    const video = document.getElementById('video');
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }
    });
    video.srcObject = stream;

    video.onloadedmetadata = () => {
      video.play();
      startQRScan();
    };
  } catch (error) {
    console.error('カメラを起動できませんでした:', error);
    alert(`カメラを起動できませんでした。エラー内容: ${error.message}`);
  }
}

function startQRScan() {
  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');

  qrScanInterval = setInterval(() => {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
      const code = jsQR(imageData.data, canvas.width, canvas.height);

      if (code) {
        alert(`QRコードを読み取りました: ${code.data}`);
        stopCamera();
      }
    }
  }, 500);
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