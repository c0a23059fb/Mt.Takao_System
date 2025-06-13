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
        const code = jsQR(imageData.data, canvas.width, canvas.height);
        if (code) {
          console.log("QRコード文字列:", code.data);
          // 文字列だけサーバーに送る方法に切り替え可能
          sendQRData(code.data);
          stopCamera();
        }
        stopCamera(); // カメラ停止

        // canvas → base64
        const base64Image = canvas.toDataURL("image/png");

        // サーバーにPOST送信
        fetch("/scan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: base64Image })
        })
        .then(res => res.json())
        .then(data => {
          if (data.redirect) {
            window.location.href = data.redirect; // 成功・失敗に応じて遷移
          } else {
            alert("予期しないエラーです: " + (data.error || "不明"));
          }
        })
        .catch(err => {
          console.error("通信エラー:", err);
          alert("サーバーとの通信に失敗しました");
        });
      }
    }
  }, 500);
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

function navigateToHome() {
  stopCamera();
  window.location.href = "/";
}

// 🔽 QRコードをFlaskに送信して画面遷移を処理
function sendQRData(qrText) {
  fetch("/scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code: qrText })  // QRの内容を送信
  })
    .then(response => response.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect;  // 成功・失敗に応じて遷移
      } else {
        alert("予期せぬ応答です");
      }
    })
    .catch(error => {
      console.error("通信エラー:", error);
      alert("QRコードの送信に失敗しました");
    });
}

// ページ離脱時にカメラを停止
window.addEventListener('pagehide', stopCamera);