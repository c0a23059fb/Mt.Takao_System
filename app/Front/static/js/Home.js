document.addEventListener("DOMContentLoaded", function() {
    const navigateTo = (url) => {
        window.location.href = url;
    };

    // Add click event listeners
    document.getElementById("navigate-qr").addEventListener("click", () => navigateTo("/camera"));
    document.getElementById("navigate-coupons").addEventListener("click", () => navigateTo("/coupons"));
    document.getElementById("navigate-shop").addEventListener("click", () => navigateTo("/shop"));
    document.getElementById("navigate-checkpoint").addEventListener("click", () => navigateTo("/checkpoint"));
});

function searchShops() {
  const keyword = document.getElementById('searchInput').value;
  const results = shops.filter(shop =>
    shop.name.includes(keyword) || shop.category.includes(keyword)
  );
  const output = results.map(r => `<p>${r.name} (${r.category})</p>`).join('');
  document.getElementById('searchResults').innerHTML = output || "<p>該当なし</p>";
}

function connectQR() {
  // QRコード読み取りページに遷移
  window.location.href = "/qr_road";
}

function showShopSearch() {
  // 周辺店舗検索ページに遷移
  window.location.href = "/shop";
}

function navigateToCoupons() {
  window.location.href = "/coupons"; // クーポン画面に遷移
}
