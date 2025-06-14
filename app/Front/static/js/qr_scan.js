async function capturePhoto() {
  if (!video.videoWidth || !video.videoHeight) {
    alert('カメラ映像の準備ができていません。少し待ってください。');
    return;
  }

  const btn = document.querySelector('.camera-btn');
  btn.disabled = true;  // 連打防止

  const canvas = document.getElementById('snapshot');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imgData = canvas.toDataURL('image/png');

  showLoading();

  try {
    const response = await fetch('/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: imgData }),
    });
    const result = await response.json();
    hideLoading();

    showResult(result.success);

    // videoが停止していたら再生を試みる
    if (video.paused || video.readyState < 3) {
      try {
        await video.play();
      } catch (e) {
        console.warn('動画再生復帰エラー:', e);
      }
    }
  } catch (error) {
    hideLoading();
    alert('通信エラー: ' + error.message);
  }

  btn.disabled = false;
}