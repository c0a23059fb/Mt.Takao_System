window.onload = () => {
  const button = document.getElementById('camera-toggle');
  button.textContent = "カメラ起動";
};

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
        console.log("読み取ったQRコード文字列:", code.data);
        sendQRDataToFlask(code.data);
        stopCamera();
      }
    }
  }, 500);
}

function sendQRDataToFlask(qrText) {
  fetch("/scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code: qrText })
  })
  .then(response => response.json())
  .then(data => {
    console.log("サーバーからの応答:", data);
  })
  .catch(error => {
    console.error("サーバー通信エラー:", error);
    alert("QRコードの送信に失敗しました");
  });
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
    document.getElementById('video').srcObject = null;
  }
  stopQRScan();
}

function stopQRScan() {
  if (qrScanInterval) {
    clearInterval(qrScanInterval);
    qrScanInterval = null;
  }
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

window.addEventListener('pagehide', stopCamera);